''''
automated data request to eBird using Playwright for session/cookie management.
handles login and cookie storage + grabbing data from eBird barchart websites for specific hotspots.
'''
##### imports
import os
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()
EBIRD_API_KEY = os.getenv('EBIRD_API_KEY')
EBIRD_USERNAME = os.getenv('EBIRD_USERNAME')
EBIRD_PASSWORD = os.getenv('EBIRD_PASSWORD')
SESSION_FILE = os.getenv('SESSION_FILE')
# set to false to watch what the BROWSERs are doing
HEADLESS = True

##### helper functions
# check if we need to get cookies again
async def is_session_valid(BROWSER):
    # do the cookies exist
    if not os.path.exists(SESSION_FILE):
        return False
    # if they do, try to ping a force login page and see if it redirects us
    context = None
    try:
        # await the context creation
        context = await BROWSER.new_context(storage_state=SESSION_FILE)
        request_context = context.request 
        # await the get request with strict timeout
        response = await request_context.get("https://ebird.org/prefs", timeout=15000)

        if "login" in response.url:
            return False
        return True
    except Exception:
        return False
    finally:
        if context:
            await context.close()
            
session_lock = asyncio.Lock()
import time
LAST_SESSION_CHECK = 0

# get new cookies via playwright
async def ensure_session(BROWSER):
    global LAST_SESSION_CHECK
    
    # fast path: in memory cache to allow parallel workers
    if time.time() - LAST_SESSION_CHECK < 300:
        return

    async with session_lock:
        # check again after acquiring lock (double-checked locking)
        if time.time() - LAST_SESSION_CHECK < 300:
            return

        # perform the slow network check (once per 5 mins)
        if await is_session_valid(BROWSER):
            LAST_SESSION_CHECK = time.time()
            return

        print("[cookies] | session expired. autologging into ebird to restore cookies...")

        context = None
        page = None
        try:
            context = await BROWSER.new_context()
            page = await context.new_page()

            # optimize: block unnecessary resources
            async def route_intercept(route):
                if route.request.resource_type in ["image", "stylesheet", "font", "media"]:
                    await route.abort()
                else:
                    await route.continue_()
            
            await page.route("**/*", route_intercept)

            await page.goto('https://secure.birds.cornell.edu/cassso/login?service=https%3A%2F%2Febird.org%2Flogin%2Fcas%3Fportal%3Debird&locale=en_US', timeout=60000)  # 60s for slow cloud

            await page.wait_for_selector('input[name="username"]', timeout=60000)  # 60s for cold starts

            ## automated login
            await page.click('input[name="username"]', timeout=5000) 
            await page.fill('input[name="username"]', EBIRD_USERNAME, timeout=5000)
            await asyncio.sleep(2)  # longer wait for cloud environments

            await page.keyboard.press("Tab")

            await page.fill('input[name="password"]', EBIRD_PASSWORD, timeout=5000)
            await asyncio.sleep(2)  # longer wait for cloud environments

            await page.keyboard.press("Enter")

            await asyncio.sleep(5) # longer wait for redirect on cloud

            # save the cookies
            await context.storage_state(path=SESSION_FILE)
            LAST_SESSION_CHECK = time.time()
            print("[cookies] | session refreshed.")

        except Exception as e:
            print(f"[error] | login failed: {e}")
        finally:
            if page: await page.close()
            if context: await context.close()
            
# limit concurrent eBird connections to preventing banning/timeouts
# default to 2 to be safe on weak hardware
concurrency_limit = int(os.getenv('EBIRD_CONCURRENCY', '2'))
print(f"[config] | EBIRD_CONCURRENCY set to {concurrency_limit}")
EBIRD_SEMAPHORE = asyncio.Semaphore(concurrency_limit)

async def fetch_data(BROWSER, loc, start, end):
    async with EBIRD_SEMAPHORE:
        context = None
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                context = await BROWSER.new_context(storage_state=SESSION_FILE)
                data_url = f"https://ebird.org/barchartData?r={loc}&byr={start}&eyr={end}&bmo=1&emo=12&fmt=tsv"
                
                request_context = context.request
                response = await request_context.get(data_url, timeout=30000)
                data_text = await response.text()

                if "<!doctype html>" in data_text.lower():
                    raise Exception(f"eBird blocked the request (got HTML). Try again later.")

                return data_text
            except Exception as e:
                if context:
                    await context.close()
                    context = None
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                else:
                    print(f"[error] | fetch failed for {loc}: {e}")
                    raise
            finally:
                if context:
                    await context.close()