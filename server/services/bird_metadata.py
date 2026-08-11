import csv
import os
import json
import asyncio
import re
from rapidfuzz import fuzz
from playwright.async_api import async_playwright

TAXONOMY_FILE = 'server/data/eBird_taxonomy_v2025.csv'
METADATA_CACHE_FILE = 'server/data/bird_metadata_cache.json'

## cache
_bird_cache = {}
_taxonomy_list = []

def extract_macaulay_asset_id(image_url): 
    """Extract the Macaulay Library asset ID from an image URL.""" 
    if not image_url: 
        return None 

    match = re.search(r"/asset/(\d+)", image_url) 

    if match: 
        photographer = match.group(1).strip()

        if " eBird " in photographer:
            photographer = photographer.split(" eBird ")[0].strip()

        return photographer
    return None

def load_metadata_cache():
    # loads json cache and populates _bird_cache
    global _bird_cache
    if os.path.exists(METADATA_CACHE_FILE):
        try:
            with open(METADATA_CACHE_FILE, 'r') as f:
                data = json.load(f)
                for code, info in data.items():
                    # cache image url
                    if info.get('imageUrl'):
                        _bird_cache[f"img_{code}"] = info['imageUrl']
                    if info.get('photographer'):
                        _bird_cache[f"photographer_{code}"] = info['photographer']
                    # cache bird code lookup (name / code)
                    if info.get('comName'):
                        _bird_cache[info['comName']] = (code, info.get('speciesUrl'))
                
                print(f"[info] | loaded {len(data)} items from metadata cache")
        except Exception as e:
            print(f"[warning] | failed to load cache: {e}")

# attempt load on import
load_metadata_cache()

def load_taxonomy():
    # loads taxonomy csv into memory
    global _taxonomy_list
    if _taxonomy_list:
        return _taxonomy_list

    if not os.path.exists(TAXONOMY_FILE):
        print(f"[error] | taxonomy file not found at: {TAXONOMY_FILE}")
        return []

    print(f"[info] | loading taxonomy from {TAXONOMY_FILE}...")
    
    try:
        loaded_birds = []
        with open(TAXONOMY_FILE, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('CATEGORY') == 'species':
                    loaded_birds.append({
                        'comName': row['PRIMARY_COM_NAME'],
                        'code': row['SPECIES_CODE']
                    })
        
        _taxonomy_list = loaded_birds
        print(f"[info] | loaded {len(_taxonomy_list)} species from CSV")
        return _taxonomy_list

    except Exception as e:
        print(f"[error] | failed to parse CSV: {e}")
        return []

def build_species_url(bird_code):
    return f"https://ebird.org/species/{bird_code}" if bird_code else None

def get_bird_code(species_name):
    # resolve species name to ebird code
    if species_name in _bird_cache:
        return _bird_cache[species_name]
    
    birds = load_taxonomy()
    if not birds:
        return None, None

    ## exact match
    species_lower = species_name.lower()
    for bird in birds:
        if bird['comName'].lower() == species_lower:
            result = (bird['code'], build_species_url(bird['code']))
            _bird_cache[species_name] = result
            return result

    ## fuzzy fallback 
    best_match = None
    best_score = 0
    
    for bird in birds:
        score = fuzz.ratio(species_lower, bird['comName'].lower())
        if score > 85: 
            if score > best_score:
                best_score = score
                best_match = bird['code']
            if score == 100: 
                break
    
    if best_match:
        result = (best_match, build_species_url(best_match))
        _bird_cache[species_name] = result
        return result
        
    _bird_cache[species_name] = (None, None)
    return None, None

async def get_species_image_url(bird_code, browser_page=None):
    # scrapes image url via playwright
    if not bird_code or not browser_page:
        return None
    
    cache_key = f"img_{bird_code}"

    photographer_cache_key = f"photographer_{bird_code}"

    if cache_key in _bird_cache and _bird_cache[cache_key] is not None:
        if photographer_cache_key in _bird_cache:
         #   print(f"[debug] | cached photographer for {bird_code}: {_bird_cache[photographer_cache_key]}")
       
            return _bird_cache[cache_key]

    print(f"[info] | fetching image for {bird_code}...")

    try:
        url = build_species_url(bird_code)
        print(f"[debug] | navigating to {url}...")
        
        # block requests to save bandwidth
        async def route_intercept(route):
            if route.request.resource_type in ["image", "stylesheet", "font", "media"]:
                await route.abort()
            else:
                await route.continue_()
        
        await browser_page.route("**/*", route_intercept)

        await browser_page.goto(url, timeout=15000, wait_until='domcontentloaded')
        
        selector = 'img.Species-media-image'
        try:
            await browser_page.wait_for_selector(selector, timeout=6000)
            img = await browser_page.query_selector(selector)
            if img:
                src = await img.get_attribute('src')


                print(f"[debug] | IMAGE URL: {src}")

                asset_id = extract_macaulay_asset_id(src)

                print(f"[debug] | MACAULAY ASSET ID: {asset_id}")

                if not src:
                    return None

                #get asset ID
                asset_id = extract_macaulay_asset_id(src)
                print(f"[debug] | Macaulay asset ID for {bird_code}: " f"{asset_id}")

                #find photographer
                photographer = None

                try: 
                    # Walk upward until we find the image's media container. 
                    photographer = await img.evaluate("""
                        (element) => {
                            let current = element;

                            for (let i = 0; i < 5 && current; i++) {
                                const text = current.innerText || "";

                                if (text.includes("©")) {
                                    const match = text.match(/©\\s*([^\\n]+)/);

                                    if (match) {
                                        let photographer = match[1].trim();

                                        if (photographer.includes(" eBird ")) {
                                            photographer = photographer.split(" eBird ")[0].trim();
                                        }

                                        return photographer;
                                    }
                                }

                                current = current.parentElement;
                            }

                            return null;
                        }
                    """)

                except Exception as e:
                    print(
                        f"[warning] | failed to find photographer "
                        f"for {bird_code}: {e}"
                    ) 
                    


                _bird_cache[cache_key] = src


                _bird_cache[photographer_cache_key] = photographer


                print(f"[success] | found image for {bird_code}: {src[:80]}...")


                if photographer: 
                    print( f"[success] | photographer for {bird_code}: " f"{photographer}" ) 

                else: print( f"[warning] | no photographer found for " f"{bird_code}" )


                return src
        except Exception as e:
            print(f"[warning] | timeout waiting for image selector for {bird_code}: {e}")
            pass 
            
        return None

    except Exception as e:
        print(f"[error] | image fetch error {bird_code}: {e}")
        return None



def get_cached_photographer(bird_code): 
    if not bird_code: 
        return None 
    
    return _bird_cache.get( 
        f"photographer_{bird_code}" 
    )


    

async def enrich_data(species_list):
    # populates image urls for top 3 birds (uses shared browser)
    enriched = []
    load_taxonomy()
    
    browser = None
    page = None
    
    # check if we need to open browser
    # logic: only open if we have top 3 birds that are NOT in cache
    should_launch = False
    
    for i in range(min(3, len(species_list))):
        rec = species_list[i]
        s_name = rec.get('Species')
        if s_name:
            # try to resolve code to check cache
            b_code, _ = get_bird_code(s_name)
            if b_code:
                cache_key = f"img_{b_code}"
                if cache_key not in _bird_cache:
                    should_launch = True
                    break
            else:
                # probably a very obscure bird, skip it
                pass

    # async context manager handles pulling up and tearing down browser
    if should_launch:
        from services.browser_manager import get_browser
        try:
            print(f"[info] | using shared browser for image fetching...")
            browser = await get_browser()
            page = await browser.new_page(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        except Exception as e:
            print(f"[error] | failed to get browser: {e}")
            import traceback
            traceback.print_exc()
            page = None

        try:
            for idx, record in enumerate(species_list):
                species_name = record.get('Species', '')
                
                if species_name:
                    # get code
                    bird_code, species_url = get_bird_code(species_name)
                    
                    record['birdCode'] = bird_code
                    record['speciesUrl'] = species_url
                    
                    # get image for top 3 birds
                    cache_key = f"img_{bird_code}"
                    
                    
                    if idx < 3 and bird_code:
                        # check cache first
                        if cache_key in _bird_cache:
                            record['imageUrl'] = _bird_cache[cache_key]


                            record['photographer'] = _bird_cache.get(f"photographer_{bird_code}")

                            print(
                                f"[debug] | {species_name} photographer: "
                                f"{record['photographer']}"
                            )


                        elif page:
                            print(f"[info] | fetching image for top bird #{idx+1}: {species_name}")
                            record['imageUrl'] = await get_species_image_url(bird_code, browser_page=page)


                            record['photographer'] = _bird_cache.get(f"photographer_{bird_code}")


                        else:
                            record['imageUrl'] = None
                            record['photographer'] = None
                    else:
                        # outside top 3, check cache only
                        if cache_key in _bird_cache:
                            record['imageUrl'] = _bird_cache[cache_key]
                            record['photographer'] = _bird_cache.get(f"photographer_{bird_code}")
                        else:
                            record['imageUrl'] = None
                            record['photographer'] = None
                else:
                    record['birdCode'] = None
                    record['speciesUrl'] = None
                    record['imageUrl'] = None
                    record['photographer'] = None
                
                enriched.append(record)
        
        finally:
            if page:
                await page.close()
    else:
        # were cached, dont need to launch browser
        for idx, record in enumerate(species_list):
            species_name = record.get('Species', '')
            if species_name:
                bird_code, species_url = get_bird_code(species_name)
                record['birdCode'] = bird_code
                record['speciesUrl'] = species_url
                cache_key = f"img_{bird_code}"
                photographer_cache_key = f"photographer_{bird_code}"
                if cache_key in _bird_cache:
                    record['imageUrl'] = _bird_cache[cache_key]
                else:
                    record['imageUrl'] = None
                record['photographer'] = _bird_cache.get(photographer_cache_key)
            else:
                record['birdCode'] = None
                record['speciesUrl'] = None
                record['imageUrl'] = None
                record['photographer'] = None
            enriched.append(record)

    return enriched

async def prefetch_all_metadata(limit=None):
    # helper to batch pre-fetch all metadata
    birds = load_taxonomy()
    if not birds:
        return

    print(f"[info] | starting pre-fetch for {len(birds)} species...")
    
    ## load existing cache
    existing_cache = {}
    if os.path.exists(METADATA_CACHE_FILE):
        with open(METADATA_CACHE_FILE, 'r') as f:
            existing_cache = json.load(f)
            print(f"[info] | loaded {len(existing_cache)} existing records")

    results = existing_cache.copy()
    
    async with async_playwright() as p:
        print(f"[info] | launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        to_process = birds[:limit] if limit else birds

        for i, bird in enumerate(to_process):
            ## save periodically
            if i > 0 and i % 10 == 0:
                print(f"[info] | saving progress at {i} records...")
                with open(METADATA_CACHE_FILE, 'w') as f:
                    json.dump(results, f, indent=4)
            
            species_name = bird['comName']
            bird_code = bird['code']

            ## skip if cached
            if bird_code in results and results[bird_code].get('imageUrl') and results[bird_code].get('photographer'):
                continue

            print(f"[{i+1}/{len(to_process)}] processing {species_name} ({bird_code})...")
            
            try:
                image_url = await get_species_image_url(bird_code, browser_page=page)

                photographer = _bird_cache.get( f"photographer_{bird_code}" )

                print(
                    f"[debug] | saving photographer for "
                    f"{bird_code}: {photographer}"
                )

            except:
                print(f"[warning] | metadata fetch failed for {bird_code}: {e}")
                image_url = None
                photographer = None
        
            
            results[bird_code] = {
                "comName": species_name,
                "code": bird_code,
                "imageUrl": image_url,
                "photographer": photographer,
                "speciesUrl": build_species_url(bird_code)
            }

        with open(METADATA_CACHE_FILE, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"[success] | completed pre-fetch. saved to {METADATA_CACHE_FILE}")
        
        await browser.close()

if __name__ == "__main__":
    print("starting taxonomy prefetch...")
    ## test
    #asyncio.run(prefetch_all_metadata(limit=1))

    asyncio.run(prefetch_all_metadata())