import requests
from selenium import webdriver

def get_cookies():
    # open browser for login
    print("opening browser...")
    driver = webdriver.Chrome()
    driver.set_window_size(550, 650)

    try:
        # go to cornell login screen
        driver.get('https://secure.birds.cornell.edu/cassso/login?service=https%3A%2F%2Febird.org%2Flogin%2Fcas%3Fportal%3Debird&locale=en_US')
        
        # wait for login and grab cookies
        input("press [ENTER] here after signing in... >>>")
        cookies = {c['name']: c['value'] for c in driver.get_cookies()}
        driver.quit()
        
        return cookies
        
    except Exception as e:
        print(f"error getting cookies: {e}")
        driver.quit()
        return None

def fetch_data(cookies, loc, start, end):
    
    if not cookies: return None
    print(f"fetching {loc} ({start}-{end})...")
    
    # parsing
    url = "https://ebird.org/barchartData"
    params = {
        "r": loc, 
        "byr": start, 
        "eyr": end, 
        "bmo": 1, 
        "emo": 12, 
        "fmt": "tsv"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://ebird.org/"
    }
    
    try:
        res = requests.get(url, params=params, headers=headers, cookies=cookies)
        
        # check if works
        if res.status_code == 200 and "<!doctype html>" not in res.text.lower():
            # all the data we want
            return res.text
        return None
    except Exception as e:
        print(f"request error: {e}")
        return None

def main():
    ### login
    cookies = get_cookies()
    if not cookies: return

    ### get inputs
    loc = input("enter location id (e.g. L901084): ").strip()
    if not loc: return
    
    try:
        print("leave years blank for all time")
        s_in = input("start year (YYYY): ").strip()
        e_in = input("end year (YYYY): ").strip()
        
        # defaults
        s_yr = int(s_in) if s_in else 1900
        e_yr = int(e_in) if e_in else 2025
        
    except ValueError:
        print("invalid years.")
        return

    ### fetch and download
    data = fetch_data(cookies, loc, s_yr, e_yr)
    
    if data:
        fname = f"ebird_{loc}_{s_yr}-{e_yr}.tsv"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(data)
        print(f"saved to: {fname}")
    else:
        print("failed to download data")

if __name__ == "__main__":
    main()