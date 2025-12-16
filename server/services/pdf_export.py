"""
pdf export service using playwright
"""
import asyncio
from playwright.async_api import async_playwright


async def generate_pdf(
    client_url: str,
    hotspot_id: str,
    num_top_birds: int = 10,
    show_graph: bool = True,
    show_photos: bool = True,
    start_year: int = None,
    end_year: int = None,
    start_month: int = None,
    start_week: int = None,
    end_month: int = None,
    end_week: int = None,
    custom_ranks: str = None,
    photo_ranks: str = None,
    gen_date: str = None,
) -> bytes:
    """
    generate a pdf of the printable report using playwright
    """
    # build the url with query params
    params = []
    params.append(f"numTopBirds={num_top_birds}")
    params.append(f"showGraph={'true' if show_graph else 'false'}")
    params.append(f"showPhotos={'true' if show_photos else 'false'}")
    
    if start_year is not None:
        params.append(f"startYear={start_year}")
    if end_year is not None:
        params.append(f"endYear={end_year}")
    if start_month is not None:
        params.append(f"startMonth={start_month}")
    if start_week is not None:
        params.append(f"startWeek={start_week}")
    if end_month is not None:
        params.append(f"endMonth={end_month}")
    if end_week is not None:
        params.append(f"endWeek={end_week}")
    
    # pass custom ranks
    if custom_ranks:
        params.append(f"customRanks={custom_ranks}")
    if photo_ranks:
        params.append(f"photoRanks={photo_ranks}")
    if gen_date:
        # url encode the date
        from urllib.parse import quote
        params.append(f"genDate={quote(gen_date)}")
    
    query_string = "&".join(params)
    full_url = f"{client_url}/hotspot/{hotspot_id}/print?{query_string}"
    
    print(f"[pdf_export] | Generating PDF from: {full_url[:120]}...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        try:
            # create context - tall viewport to capture all content
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 850, 'height': 11000},
                bypass_csp=True,
            )
            
            page = await context.new_page()
            
            # nav to printable report
            print(f"[pdf_export] | Navigating to page...")
            await page.goto(full_url, timeout=30000, wait_until='domcontentloaded')
            
            # wait for bird table to appear
            try:
                await page.wait_for_selector('.bird-table-section', timeout=20000)
                print(f"[pdf_export] | Data loaded")
            except:
                print("[pdf_export] | Table not found, waiting...")
                await asyncio.sleep(3)
            
            # wait for render
            await asyncio.sleep(1)
            
            # generate pdf
            pdf_bytes = await page.pdf(
                format='Letter',
                print_background=True,
                margin={
                    'top': '0.4in',
                    'bottom': '0.4in',
                    'left': '0.5in',
                    'right': '0.5in'
                },
            )
            
            print(f"[pdf_export] | PDF generated successfully, size: {len(pdf_bytes)} bytes")
            return pdf_bytes
            
        finally:
            await browser.close()
