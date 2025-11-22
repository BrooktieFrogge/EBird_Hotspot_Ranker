'''
main ranker script. uses data_request.py to fetch data and rank_calculator.py calculate ranks. currently creates result_dict for a single location.
'''
##### imports
import data_request 
import rank_calculator
import pandas as pd
import os
from playwright.sync_api import sync_playwright

### config
SAVE_FILE = True

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

##### main function
def main():
    print("=" * 15)
    print("  eBird Ranker")
    print("=" * 15)

    while True:

        ## user inputs
        ## TODO: replace with function args for API use
        loc_input = input("[input] | enter location id (e.g. L901084), 'batch' for batch input, or 'q' to quit: ").strip().upper()
        if loc_input.lower() == 'q': break
        
        if loc_input == 'BATCH':
            batch_choice = input("[input] | load from file (f) or create new (n)? ").strip().upper()
            if batch_choice == 'N':
                process_list = create_locations()
            elif batch_choice == 'F':
                process_list = load_locations()
            if not process_list: continue
        elif loc_input:
            process_list = [loc_input.upper()]
        else:
            continue

        try:
            print("[info] | leave years blank for all time")
            start_yr_in = input("[input] | start year (YYYY): ").strip()
            end_yr_in = input("[input] | end year (YYYY): ").strip()

            # defaults
            start_yr = int(start_yr_in) if start_yr_in else 1900
            end_yr = int(end_yr_in) if end_yr_in else 2025

        except ValueError:
            print("[error] | invalid years.")
            continue

        ## fetch data
        print(f"\n[info] | starting process for {len(process_list)} locations...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=data_request.HEADLESS)

            # ensure session is valid, autologin if needed
            data_request.ensure_session(browser)

            for loc in process_list:
                print(f"[info] | fetching {loc} data from ebird...")
                raw_data = data_request.fetch_data(browser, loc, start_yr, end_yr)

                # process in memory
                if raw_data:
                    try:
                        # pass data + inputs to calculator
                        result_dict = rank_calculator.process_data(raw_data, loc, start_yr, end_yr, save=SAVE_FILE)
                        
                        if SAVE_FILE:
                            print(f"[success] | saved results to '{rank_calculator.OUTPUT_DIR}'")
                        else:
                            # convert the dict back to df just to show head in logs
                            df = pd.DataFrame(result_dict['data'])
                            print(f"[success] | results stored in result_dict (location: {result_dict['location']})")
                            print(df.head(10))
                    except Exception as e:
                        print(f"[error] | calculation/formatting failed - {e}")
                else:
                    print("[error] | no data found.")

# run main
if __name__ == "__main__":
    main()