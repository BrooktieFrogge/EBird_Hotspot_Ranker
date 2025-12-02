'''
automated data request to eBird using Playwright for session/cookie management.
handles login and cookie storage + grabbing data from eBird barchart websites for specific hotspots.
'''
##### imports
import os
import time
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv('server/.env')
EBIRD_API_KEY = os.getenv('EBIRD_API_KEY')
EBIRD_USERNAME = os.getenv('EBIRD_USERNAME')
EBIRD_PASSWORD = os.getenv('EBIRD_PASSWORD')
SESSION_FILE = os.getenv('SESSION_FILE')
# set to false to watch what the BROWSERs are doing
HEADLESS = False

##### helper functions
# check if we need to get cookies again
def is_session_valid(BROWSER):
    # do the cookies exist
    if not os.path.exists(SESSION_FILE):
        return False
    # if they do, try to ping a force login page and see if it redirects us
    try:
        context = BROWSER.new_context(storage_state=SESSION_FILE)
        response = context.request.get("https://ebird.org/prefs")
        if "login" in response.url:
            return False
        return True
    except Exception:
        return False
    finally:
        if 'context' in locals():
            context.close()
            
# get new cookies via playwright
def ensure_session(BROWSER):
    if is_session_valid(BROWSER):
        print("[cookies] | existing session ok. using saved cookies.")
        return

    print("[cookies] | session expired. autologging into ebird to restore cookies...")

    context = None
    page = None
    try:
        context = BROWSER.new_context()
        page = context.new_page()
        page.goto('https://secure.birds.cornell.edu/cassso/login?service=https%3A%2F%2Febird.org%2Flogin%2Fcas%3Fportal%3Debird&locale=en_US')

        page.wait_for_selector('input[name="username"]', timeout=5000)

        ## automated login
        print("[playwright] | typing .env username...")
        page.click('input[name="username"]') 
        page.fill('input[name="username"]', EBIRD_USERNAME)
        time.sleep(1) 

        page.keyboard.press("Tab")

        print("[playwright] | typing .env password...")
        page.fill('input[name="password"]', EBIRD_PASSWORD)
        time.sleep(1) 

        page.keyboard.press("Enter")

        print("[playwright] | submitted. redirecting...")
        time.sleep(3) # wait for redirect

        # save the cookies
        context.storage_state(path=SESSION_FILE)
        print("[cookies] | playwright login success! session saved.")

    except Exception as e:
        print(f"[error] | .env login skipped or failed: {e}")
    finally:
        if page: page.close()
        if context: context.close()

def fetch_data(BROWSER, loc, start, end):
    print(f"[input] | connecting to eBird for {loc} ({start}-{end})...")
    print("[info] | downloading data...")

    context = None
    try:
        context = BROWSER.new_context(storage_state=SESSION_FILE)
        data_url = f"https://ebird.org/barchartData?r={loc}&byr={start}&eyr={end}&bmo=1&emo=12&fmt=tsv"
        response = context.request.get(data_url)
        data_text = response.text()

        if "<!doctype html>" in data_text.lower():
    
            return None

        return data_text
    finally:
        if context: context.close()