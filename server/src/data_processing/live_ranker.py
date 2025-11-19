import data_request 
import rank_calculator
import pandas as pd

SAVE_FILE = False

def main():
    print("=" * 15)
    print("  eBird Ranker")
    print("=" * 15)

    ## login
    cookies = data_request.get_cookies()
    if not cookies:
        print("[error] | login failed.")
        return

    while True:

        ## inputs
        loc = input("[input] | enter location id (e.g. L901084 or 'q' to quit): ").strip()
        if loc.lower() == 'q': break
        if not loc: continue

        try:
            print("leave years blank for all time")
            start_yr_in = input("[input] | start year (YYYY): ").strip()
            end_yr_in = input("[input] | end year (YYYY): ").strip()

            # defaults
            start_yr = int(start_yr_in) if start_yr_in else 1900
            end_yr = int(end_yr_in) if end_yr_in else 2025

        except ValueError:
            print("[error] | invalid years.")
            continue

        ## fetch data
        print("fetching from ebird...")
        raw_data = data_request.fetch_data(cookies, loc, start_yr, end_yr)

        ## process in memory
        if raw_data:
            print(f"calculating rankings for {loc}...")
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

if __name__ == "__main__":
    main()