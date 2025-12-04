'''
main ranker script. uses data_request.py to fetch data and rank_calculator.py calculate ranks. currently creates result_dict for a single location.
'''
##### imports
from  services.ranking_engine.rank_calculator import process_data
from  services.ranking_engine.fetch_barcharts import fetch_data,ensure_session,HEADLESS
import pandas as pd
import os,httpx
from playwright.sync_api import sync_playwright

### config
SAVE_FILE = True
BROWSER = None

##### helper functions
# load locations from a text file
def load_locations(filepath=None):
    if filepath is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, 'ebird_in', 'locations.txt')
        
    try:
        with open(filepath, 'r') as f:
            return [line.strip().upper() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"[error] | '{filepath}' was not found.")
        return []
# create locations via user input
def create_locations():
    location_list = []
    print("\n[input] | enter eBird location IDs one at a time.")
    print("[input] | type 'done' or 'q' when finished.")
    
    while True:
        loc_input = input(f"[input] | ID #{len(location_list) + 1} (or 'done'): ").strip().upper()
        
        if loc_input in ('DONE', 'Q'):
            break
        
        if loc_input.startswith('L') and loc_input[1:].isdigit():
            location_list.append(loc_input)
        elif loc_input:
            print("[error] | invalid ID format, must start with 'L' followed by numbers.")

    return location_list

#TODO add type checking & error handling for weeks
##### main function
def get_rankings(locId:int, start_yr:int| None = None, end_yr:str| None = None):

        # if loc_input == 'BATCH':
        #     batch_choice = input("[input] | load from file (f) or create new (n)? ").strip().upper()
        #     if batch_choice == 'N':
        #         process_list = create_locations()
        #     elif batch_choice == 'F':
        #         process_list = load_locations()
        #     if not process_list: continue
        # elif loc_input:
        process_list = [locId.upper()]
       
        try:
        
            start_yr = start_yr if start_yr else 1900
            end_yr = end_yr if end_yr else 2025

        except Exception as e:
             return(f"Invalid Daterange - {e}.")
  
        with sync_playwright() as p:
            BROWSER =  p.chromium.launch(headless= HEADLESS)

            # ensure session is valid, autologin if needed
            ensure_session(BROWSER)

            for loc in process_list:
                # print(f"[info] | fetching {loc} data from ebird...")
                raw_data = fetch_data(BROWSER, loc, start_yr, end_yr)

                # process in memory
                if raw_data:
                    try:
                        # pass data + inputs to calculator
                        result_dict = process_data(raw_data, loc, start_yr, end_yr, save=SAVE_FILE)

                        if SAVE_FILE:
                            print ({"Request Status":"[success] | saved results to '{rank_calculator.OUTPUT_DIR}'"})
                            return result_dict
                    
                        else:
                            # convert the dict back to df just to show head in logs
                            df = pd.DataFrame(result_dict['data'])

                            return{f"[success] | results stored in result_dict (location: {result_dict['location']})": df.head(10)}
                        
                    except Exception as e:
                        return(f"[error] | calculation/formatting failed - {e}")
                         
                else:
                    return None