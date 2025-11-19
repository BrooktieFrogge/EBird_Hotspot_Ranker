import data_request 
import rank_calculator     

def main():
    print("=" * 15)
    print("  eBird Ranker")
    print("=" * 15)

    ## login
    cookies = data_request.get_cookies()
    if not cookies:
        print("login failed.")
        return

    while True:

        ## inputs
        loc = input("enter location id (e.g. L901084 or 'q' to quit): ").strip()
        if loc.lower() == 'q': break
        if not loc: continue

        try:
            print("leave years blank for all time")
            s_in = input("start year (YYYY): ").strip()
            e_in = input("end year (YYYY): ").strip()

            # defaults
            s_yr = int(s_in) if s_in else 1900
            e_yr = int(e_in) if e_in else 2025

        except ValueError:
            print("invalid years.")
            continue

        ## fetch data
        print("fetching from ebird...")
        raw_data = data_request.fetch_data(cookies, loc, s_yr, e_yr)

        ## process in memory
        if raw_data:
            print(f"calculating rankings for {loc}...")
            try:
                # pass data + inputs to calculator
                #rank_calculator.process_data(raw_data, loc, s_yr, e_yr)
                
                print(f"success: saved results to '{rank_calculator.OUTPUT_DIR}'")
            except Exception as e:
                print(f"error: calculation failed - {e}")
        else:
            print(" error: no data found.")

if __name__ == "__main__":
    main()