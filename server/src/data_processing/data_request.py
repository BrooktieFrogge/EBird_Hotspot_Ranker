import os
import time
from playwright.sync_api import sync_playwright

# this is the 'database' right now
SESSION_FILE = 'ebird_session.json'
# set to false to watch what the browsers are doing
HEADLESS = True

# helper function to skip login
def is_session_valid():
    # do the cookies exist
    if not os.path.exists(SESSION_FILE):
        return False
    # if they do, try to ping a force login page and see if it redirects us
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        try:
            context = browser.new_context(storage_state=SESSION_FILE)
            response = context.request.get("https://ebird.org/prefs")
            if "login" in response.url:
                return False
            return True
        except:
            return False
        finally:
            browser.close()
            
def fetch_data(loc, start, end, username=None, password=None):
    print(f"[input] | connecting to eBird for {loc} ({start}-{end})...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        
        ### check if a session exists
        if os.path.exists(SESSION_FILE):
            print("[cookies] | found saved session, skipping login...")
            context = browser.new_context(storage_state=SESSION_FILE)
        else:
            print("[cookies] | no session found, starting fresh...")
            context = browser.new_context()

        ### login if we dont have a valid sessions (meaning creds got passed in)
        if username and password:
            print("[cookies] | logging into ebird to grab cookies]...")

            page = context.new_page()
            page.goto('https://secure.birds.cornell.edu/cassso/login?service=https%3A%2F%2Febird.org%2Flogin%2Fcas%3Fportal%3Debird&locale=en_US')

            try:
                page.wait_for_selector('input[name="username"]', timeout=5000)
                
                ## automated login
                print("[playwright] | typing username...")
                page.click('input[name="username"]') 
                page.fill('input[name="username"]', username)
                time.sleep(1) 

                page.keyboard.press("Tab")

                print("[playwright] | typing password...")
                page.fill('input[name="password"]', password)
                time.sleep(1) 

                page.keyboard.press("Enter")
                
                print("[playwright] | submitted. redirecting...")
                time.sleep(5)

                # save the cookies
                context.storage_state(path=SESSION_FILE)
                print("[cookies] | playwright login success! session saved.")

            except Exception as e:
                print(f"[error] | login skipped or failed: {e}")

            page.close()

        ### fetch data
        data_url = f"https://ebird.org/barchartData?r={loc}&byr={start}&eyr={end}&bmo=1&emo=12&fmt=tsv"
        print("[info] | downloading data...")
        response = context.request.get(data_url)
        data_text = response.text()

        # debug
        browser.close()
        if "<!doctype html>" in data_text.lower():
            print("[error] | something went wrong. either bad location ID or invalid cookies.")
            return None

        return data_text