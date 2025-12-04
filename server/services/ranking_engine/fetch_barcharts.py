''''
automated data request to eBird using Playwright for session/cookie management.
handles login and cookie storage + grabbing data from eBird barchart websites for specific hotspots.
'''
##### imports
import os
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv('server/.env')
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
        # await the get request
        response = await request_context.get("https://ebird.org/prefs")

        if "login" in response.url:
            return False
        return True
    except Exception:
        return False
    finally:
        if context:
            await context.close()
            
# get new cookies via playwright
async def ensure_session(BROWSER):
    # await the session check
    if await is_session_valid(BROWSER):
        print("[cookies] | existing session ok. using saved cookies.")
        return

    print("[cookies] | session expired. autologging into ebird to restore cookies...")

    context = None
    page = None
    try:
        context = await BROWSER.new_context()
        page = await context.new_page()
        await page.goto('https://secure.birds.cornell.edu/cassso/login?service=https%3A%2F%2Febird.org%2Flogin%2Fcas%3Fportal%3Debird&locale=en_US')

        await page.wait_for_selector('input[name="username"]', timeout=5000)

        ## automated login
        print("[playwright] | typing .env username...")
        await page.click('input[name="username"]') 
        await page.fill('input[name="username"]', EBIRD_USERNAME)
        await asyncio.sleep(1) 

        await page.keyboard.press("Tab")

        print("[playwright] | typing .env password...")
        await page.fill('input[name="password"]', EBIRD_PASSWORD)
        await asyncio.sleep(1) 

        await page.keyboard.press("Enter")

        print("[playwright] | submitted. redirecting...")
        await asyncio.sleep(3) # wait for redirect

        # save the cookies
        await context.storage_state(path=SESSION_FILE)
        print("[cookies] | playwright login success! session saved.")

    except Exception as e:
        print(f"[error] | .env login skipped or failed: {e}")
    finally:
        if page: await page.close()
        if context: await context.close()

async def fetch_data(BROWSER, loc, start, end):
    print(f"[input] | connecting to eBird for {loc} ({start}-{end})...")
    print("[info] | downloading data...")

    context = None
    try:
        context = await BROWSER.new_context(storage_state=SESSION_FILE)
        data_url = f"https://ebird.org/barchartData?r={loc}&byr={start}&eyr={end}&bmo=1&emo=12&fmt=tsv"
        
        request_context = context.request
        response = await request_context.get(data_url)
        data_text = await response.text()

        if "<!doctype html>" in data_text.lower():
            # session might be invalid or page failed to load properly
            return None

        return data_text
    finally:
        if context: await context.close()