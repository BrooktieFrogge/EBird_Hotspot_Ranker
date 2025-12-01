from services.hotspot_search import search_hotspots
import os,httpx
from datetime import datetime, timedelta, date
import asyncio

headers = {"X-eBirdApiToken":os.getenv("EBIRD_API_KEY")}
#limit concurrent API calls to prevent exceeding rate limits
SEMAPHORE = asyncio.Semaphore(5)

'''
Returns recent (prev 30 days) eBird hotspot checklist info
ex. input: L1150539 -hotspotID

Returns: dictionary of checklist data for the specified hotspot
'''

async def get_recent_checklists(hotspotID:str):
   #get recent data for last 30 days
    default_end = date.today().strftime("%Y-%m-%d")
    default_start = (date.today() - timedelta(days=29)).strftime("%Y-%m-%d")

    return await get_dateRange(hotspotID,default_start,default_end)

'''
Fetch observations for a single day.

- handles 429/503 rate limit errors using exponential backoff
- response filtering 
- concurrency limiting using sempahore

Returns: list of filterd checklist dictionaries including :
-hotspot location id
-checklist submissions id
-observation date
-how many of the species were seen on date in hotspot
-species code
-species common name
'''
async def get_single_day(client,hotspotID:str,d:str, attempt=1):

    #protect external API from overload
    async with SEMAPHORE:
        d = datetime.strptime(d,"%Y-%m-%d").date()

        url = f"https://api.ebird.org/v2/data/obs/{hotspotID}/historic/{d.year}/{d.month}/{d.day}?hotspot=true&detail=full"

        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            #small delay to workaround limits
            await asyncio.sleep(0.25)        
            data = response.json()

            #if no sightings that day then the data is empty list
            if not isinstance(data,list):
                return []
        
            #columns to keep, shorten responses before appending
            filterby =  ['locId','subId','obsDt',
    'howMany','speciesCode','comName',]

            filtered = []

            for entry in data:
                filtered_entry = {key: entry[key] for key in filterby if key in entry}
                if filtered_entry:
                    filtered.append(filtered_entry)

            return filtered
        
        #if rate limited retry
        except httpx.HTTPStatusError as e:
            #handle overload with exponential backoff
            if e.response.status_code in (429,503) and attempt < 3:
                await asyncio.sleep(2 ** attempt)
                return await get_single_day(client,hotspotID,d,attempt+1)
            return []
        
        except Exception:
            return None

'''
Fetch checklists for a range of dates.
L1150539
2025-11-02
2025-11-12

Returns: dictionary of flattened list of checklist info for hotspot
'''
async def get_dateRange(hotspotID:str,startDate:str,endDate:str):
    #convert strings to date objects
    sd = datetime.strptime(startDate,"%Y-%m-%d").date()
    ed = datetime.strptime(endDate,"%Y-%m-%d").date()

    #generate lists of all days in range
    dates = []
    while sd<=ed:
        dates.append(sd.strftime("%Y-%m-%d"))
        sd += timedelta(days=1)

    #fetch all days concurrently and gather results
    async with httpx.AsyncClient() as client:
        tasks = [get_single_day(client,hotspotID,d) for d in dates]    

        results = await asyncio.gather(*tasks)

    #flatten list of lists
    flattened_results = [item for daily in results for item in daily]

    return flattened_results

'''
Fetch additional data about a specific hotspot
'''

async def get_metadata(hotspotID: str):
    url = f"https://api.ebird.org/v2/ref/hotspot/info/{hotspotID}"

    res = httpx.get(url,headers=headers)
    
    if res.status_code != 200:
        return None
    data = res.json()

    return {
        "locId": hotspotID,
        "name" : data["name"],
        "lat" : data["latitude"],
        "lng" : data["longitude"],
        "country" : data ["countryName"],
        "subnational1" : data ["subnational1Name"]
    }