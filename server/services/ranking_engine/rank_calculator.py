'''
calculator script. processes eBird barchart data files to compute weighted rank frequency and related metrics based on user filters. outputs results to CSV and summary text files, or returns data in a dict for API use.
'''
##### imports
import pandas as pd
import os
import re
import requests
import unicodedata
from dotenv import load_dotenv
import io
from services.bird_metadata import enrich_data

##### config
# load api key 
load_dotenv('server/.env')
EBIRD_API_KEY = os.getenv('EBIRD_API_KEY')
# paths
INPUT_DIR = 'server/data/ebird_in'
OUTPUT_DIR = 'server/data/ebird_out'

# fixed rows from ebird barchart files
MONTH_ROW_INDEX = 13
SAMPLE_SIZE_ROW_INDEX = 14
DATA_START_ROW_INDEX = 16

# month name mapping
MONTH_NAMES = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
MONTH_TO_NUM = {name: idx for idx, name in enumerate(MONTH_NAMES)}

TOP_N_VIEW = 10

##### helper functions
def month_str_to_num(month_str: str) -> int:
        if not month_str:
                return 0
        return MONTH_TO_NUM.get(month_str.strip(), 0)

def month_num_to_str(month_num: int) -> str:
        if month_num and 1 <= month_num <= 12:
                return MONTH_NAMES[month_num]
        return None

def get_location_name(loc_id):
        ## call api to convert id -> name
        url = f"https://api.ebird.org/v2/ref/hotspot/info/{loc_id}"
        headers = {'X-eBirdAPIToken': EBIRD_API_KEY}

        r = requests.get(url, headers=headers)

        if r.status_code == 200:
                data = r.json()
                return data.get('locName', 'Unknown Location')

        return 'Unknown Location'

def fix_filename_string(text):
        ## normalize text to make it filename safe
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
        text = re.sub(r'[^\w\s-]', '', text).strip().lower()
        return re.sub(r'[\s-]+', '_', text)

def create_summary(filename, source_file, total_weight, df, used_weeks, location_name):
        ## writes the summary.txt
        with open(filename, 'w', encoding='utf-8') as f:
                # top n list
                f.write(f"Top {TOP_N_VIEW} Species\n{'-'*20}\n")
                f.write(df.head(TOP_N_VIEW).to_string(index=False, float_format="%.6f"))
                f.write("\n\n")

                # stats
                f.write(f"Summary\n{'-'*20}\n")
                f.write(f"Location: {location_name}\n")
                f.write(f"Source: {source_file}\n")
                f.write(f"Total Sample Size: {total_weight}\n\n")

                # breakdown
                f.write("Weeks Used:\n")
                for k, v in used_weeks.items():
                        f.write(f"{k}: {v}\n")

##### main logic
def calculate_metrics(df, raw_weights, month_row, start_month=None, start_week=None, end_month=None, end_week=None):
        """
        filter eBird barchart data by month and week within month.
        
        args:
                df: DataFrame with species data (columns are weekly observations)
                raw_weights: list of sample sizes for each week
                month_row: row containing month headers on txt file
                start_month: month name (3letter code) or None for Jan
                start_week: week within month 1-4 or None for week 1
                end_month: month name (3letter code) or None for Dec
                end_week: Wwek within month 1-4 or None for week 4
        
        returns:
                tuple: (final_df, total_weight, used_weeks_map, cols_used_count, sample_sizes_map)
        """
        
        start_month_num = month_str_to_num(start_month) if isinstance(start_month, str) else (start_month if start_month else 1)
        end_month_num = month_str_to_num(end_month) if isinstance(end_month, str) else (end_month if end_month else 12)
        
        # default config
        if start_week is None:
                start_week = 1
        if end_week is None:
                end_week = 4
        
        # validate inputs
        start_week = max(1, min(4, int(start_week)))
        end_week = max(1, min(4, int(end_week)))
        
        ### filter columns based on month/week range
        cols_to_keep = []
        weights_to_use = []
        used_weeks_map = {} # for summary.txt
        sample_sizes_map = {} # all weekly sample sizes for frontend

        current_month = ""
        current_month_num = 0
        week_counter = 0

        # iterate through cols to decide what to keep
        for i, col_name in enumerate(df.columns[1:]): 
                month_row_index = i + 1 
                weight_index = i      

                # month headers have gaps, track the last seen month
                if month_row_index < len(month_row):
                        m = month_row[month_row_index].strip()
                        if m:
                                current_month = m
                                current_month_num = month_str_to_num(m)
                                week_counter = 1
                        else:
                                week_counter += 1

                # get this week's sample size
                w = raw_weights[weight_index] if weight_index < len(raw_weights) else 0
                week_key = f"{current_month}_w{week_counter}"
                sample_sizes_map[week_key] = w 

                # check if this (month, week) is in the range
                keep = False
                
                if current_month_num == 0:
                        keep = False  # unknown month, skip
                elif start_month_num < end_month_num:
                        # normal case:
                        if start_month_num < current_month_num < end_month_num:
                                keep = True  # middle months
                        elif current_month_num == start_month_num and week_counter >= start_week:
                                keep = True  # start month, week >= start_week
                        elif current_month_num == end_month_num and week_counter <= end_week:
                                keep = True  # end month, week <= end_week
                elif start_month_num == end_month_num:
                        # same month case
                        if current_month_num == start_month_num and start_week <= week_counter <= end_week:
                                keep = True
                else:
                        # wrap around case
                        if current_month_num >= start_month_num or current_month_num <= end_month_num:
                                if current_month_num == start_month_num and week_counter >= start_week:
                                        keep = True
                                elif current_month_num == end_month_num and week_counter <= end_week:
                                        keep = True
                                elif start_month_num < current_month_num or current_month_num < end_month_num:
                                        keep = True

                if keep:
                        cols_to_keep.append(col_name)
                        weights_to_use.append(w)
                        used_weeks_map[week_key] = w

        total_weight = sum(weights_to_use)

        ### calculate wtd_rf
        
        # ensure numeric
        df[cols_to_keep] = df[cols_to_keep].apply(pd.to_numeric, errors='coerce').fillna(0)

        # the math
        weighted_sum = (df[cols_to_keep] * weights_to_use).sum(axis=1)
        df['wtd_rf'] = weighted_sum / total_weight if total_weight > 0 else 0   
        
        ### calculate rank, rfpc
        
        final = df[['Species', 'wtd_rf']].sort_values(by='wtd_rf', ascending=False).reset_index(drop=True)
        final['Rank'] = final.index + 1

        top_score = final['wtd_rf'].iloc[0] if not final.empty else 1
        final['rfpc'] = ( final['wtd_rf'] / top_score ) * 100
        final['rfpc'] = final['rfpc'].fillna(0) # handle div by zero
        
        return final[['Rank', 'Species', 'wtd_rf', 'rfpc']], total_weight, used_weeks_map, len(cols_to_keep), sample_sizes_map

# may not be needed anymore, still good for debug
def process_file(filepath, filename, start_month=None, start_week=None, end_month=None, end_week=None):
        print(f"[calc] | processing {filename}...")

        ### read headers and sample sizes
        with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                month_row = lines[MONTH_ROW_INDEX].replace('\n', '').split('\t')
                sample_row = lines[SAMPLE_SIZE_ROW_INDEX].replace('\n', '').split('\t')

        # clean up the sample sizes
        raw_weights = []
        for x in sample_row[1:]:
                clean_x = x.strip()
                if clean_x.replace('.', '', 1).isdigit(): # checks for float or int
                        raw_weights.append(float(clean_x))
                else:
                        raw_weights.append(0.0)

        ### load into pandas

        # skip all headers, add them back later
        rows_to_skip = list(range(DATA_START_ROW_INDEX)) 

        df = pd.read_csv(
                filepath, 
                sep='\t', 
                header=None, 
                skiprows=rows_to_skip
        )
        df = df.rename(columns={0: 'Species'})
        df = df.dropna(subset=['Species'])        

        ### calculate metrics
        final, total_weight, used_weeks_map, cols_used, sample_sizes_map = calculate_metrics(
                df,
                raw_weights,
                month_row,
                start_month=start_month,
                start_week=start_week,
                end_month=end_month,
                end_week=end_week
        )

        ### save output

        # pull info for filenames
        loc_id = re.search(r'L\d+', filename).group(0)
        loc_name = get_location_name(loc_id)

        # parse date range from filename (YYYY_YYYY_M_M)
        dates = re.search(r'(\d{4})_(\d{4})_(\d)_(\d)', filename)
        date_str = ""
        if dates:
                date_str = f"_{dates.group(1)[-2:]}-{dates.group(2)[-2:]}"

        slug = fix_filename_string(loc_name)

        # save in the out dir
        out_csv = os.path.join(OUTPUT_DIR, f"rank_data_{slug}{date_str}.csv")
        out_txt = os.path.join(OUTPUT_DIR, f"summary_{slug}{date_str}.txt")

        
        final.to_csv(out_csv, index=False)
        create_summary(out_txt, filename, total_weight, final, used_weeks_map, loc_name)
        print(f"[success] | saved: {out_csv}")
        
        return final, sample_sizes_map

# fetch location data and process
async def process_data(raw_tsv, loc_id, start_year, end_year, start_month=None, start_week=None, end_month=None, end_week=None, save=True):
        """
        process eBird barchart data for API endpoint.
        
        args:
                raw_tsv: raw barchart data as TSV string from eBird API
                loc_id: location ID ('L123456')
                start_year: start year (used for fetching)
                end_year: end year (used for fetching)
                start_month: month name (3letter code) or None for Jan
                start_week: start week (1-4) or None for week 1
                end_month: month name (3-letter) or None for Dec
                end_week: end week (1-4) or None for week 4
                save: whether to save results to file
        
        returns:
                dictionary with location, total_sample_size, sample_sizes_by_week, and ranked bird data
        """
        
        print(f"[calc] | calculating rankings for {loc_id}...")
        f_stream = io.StringIO(raw_tsv)
        lines = f_stream.readlines()
        
        month_row = lines[MONTH_ROW_INDEX].replace('\n', '').split('\t')
        sample_row = lines[SAMPLE_SIZE_ROW_INDEX].replace('\n', '').split('\t')

        # clean up the sample sizes
        raw_weights = []
        for x in sample_row[1:]:
                clean_x = x.strip()
                if clean_x.replace('.', '', 1).isdigit(): 
                        raw_weights.append(float(clean_x))
                else:
                        raw_weights.append(0.0)

        ### load into pandas
        f_stream.seek(0)
        rows_to_skip = list(range(DATA_START_ROW_INDEX)) 

        df = pd.read_csv(
                f_stream, 
                sep='\t', 
                header=None, 
                skiprows=rows_to_skip
        )
        df = df.rename(columns={0: 'Species'})
        df = df.dropna(subset=['Species']) 

        ### calculate metrics
        final, total_weight, used_weeks_map, cols_used, sample_sizes_map = calculate_metrics(
                df, 
                raw_weights, 
                month_row,
                start_month=start_month,
                start_week=start_week,
                end_month=end_month,
                end_week=end_week
        )
        loc_name = get_location_name(loc_id)

        ### save output
        if save:
                slug = fix_filename_string(loc_name)
                date_str = f"_{str(start_year)[-2:]}-{str(end_year)[-2:]}"

                if not os.path.exists(OUTPUT_DIR):
                        os.makedirs(OUTPUT_DIR)

                out_csv = os.path.join(OUTPUT_DIR, f"rank_data_{slug}{date_str}.csv")
                out_txt = os.path.join(OUTPUT_DIR, f"summary_{slug}{date_str}.txt")

                final.to_csv(out_csv, index=False)
                create_summary(out_txt, f"Live Data from ({loc_id})", total_weight, final, used_weeks_map, loc_name)
                print(f"[success] | saved: {out_csv}")

        # return in a frontend stlye:
        data_records = final.to_dict('records') # converts df to a list of dicts
        
        # enrich species data with bird codes, URLs, and images for top 3
        enriched_data = await enrich_data(data_records)
        
        return {
                "location": loc_name,
                "total_sample_size": total_weight,
                "sample_sizes_by_week": sample_sizes_map,  # All weekly sample sizes for frontend display
                "data": enriched_data
        }
