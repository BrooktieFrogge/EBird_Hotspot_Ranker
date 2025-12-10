'''
main ranker script. uses data_request.py to fetch data and rank_calculator.py calculate ranks. currently creates result_dict for a single location.
'''
##### imports
from  services.ranking_engine.rank_calculator import process_data
from  services.ranking_engine.fetch_barcharts import fetch_data, ensure_session, HEADLESS
import pandas as pd
import os, httpx
from playwright.async_api import async_playwright

### config
SAVE_FILE = False
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

##### main function
async def get_rankings(
    locId: str,
    start_yr: int | None = None,
    end_yr: int | None = None,
    start_month: int | None = None,
    start_week: int | None = None,
    end_month: int | None = None,
    end_week: int | None = None
):
    """
    get bird rankings for a location with optional month/week filtering.
    
    args:
        locId: eBird location ID (e.g., 'L123456')
        start_yr: Start year for data range
        end_yr: End year for data range
        start_month: Start month (1-12)
        start_week: Start week within start_month (1-4)
        end_month: End month (1-12)
        end_week: End week within end_month (1-4)
    
    returns:
        Dictionary with location name, sample size, and ranked bird data
    """
    
    process_list = [locId.upper()]
    
    try:
        start_yr = start_yr if start_yr else 1900
        end_yr = end_yr if end_yr else 2025

    except Exception as e:
            return(f"Invalid Daterange - {e}.")

    # using async context manager
    async with async_playwright() as p:
        BROWSER = await p.chromium.launch(headless=HEADLESS)

        # await the session check
        await ensure_session(BROWSER)

        for loc in process_list:
            # await the fetch data call
            raw_data = await fetch_data(BROWSER, loc, start_yr, end_yr)

            # process in memory
            if raw_data:
                try:
                    # await the calculator process
                    result_dict = await process_data(
                        raw_data,
                        loc,
                        start_yr,
                        end_yr,
                        start_month=start_month,
                        start_week=start_week,
                        end_month=end_month,
                        end_week=end_week,
                        save=SAVE_FILE
                    )

                    if SAVE_FILE:
                        print ({"Request Status":"[success] | saved results to output directory"})
                        return result_dict
                
                    else:
                        print(f"[success] | results stored in memory: result_dict (location: {result_dict['location']})")
                        return result_dict
                    
                except Exception as e:
                    return(f"[error] | calculation/formatting failed - {e}")
                        
            else:
                return None