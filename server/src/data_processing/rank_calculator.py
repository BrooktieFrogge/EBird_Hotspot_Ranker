##### imports
import pandas as pd
import os
import re
import csv
import requests
import unicodedata
from dotenv import load_dotenv
import io

##### config

# load api key 
load_dotenv('server/.env')
EBIRD_API_KEY = os.getenv('EBIRD_API_KEY')

# paths
INPUT_DIR = 'server/src/data_processing/ebird_in'
OUTPUT_DIR = 'server/src/data_processing/ebird_out'


# fixed rows from ebird barchart files
MONTH_ROW_INDEX = 13
SAMPLE_SIZE_ROW_INDEX = 14
DATA_START_ROW_INDEX = 16

# filter config: 'Jun': [1, 2, 4] or 'Jun': 'all'
FILTER_CONFIG = {
        'Jun': 'all',
        'Jul': 'all',
        'Aug': 'all',
        'Sep': 'all'
}
TOP_N_VIEW = 10

##### helper functions

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

def process_file(filepath, filename):
        print(f"processing {filename}...")

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
        
        ### filter columns based on config
        cols_to_keep = []
        weights_to_use = []
        used_weeks_map = {} # for summary.txt

        current_month = ""
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
                                week_counter = 1
                        else:
                                week_counter += 1

                # check if we want this month/week
                keep = False
                if not FILTER_CONFIG:
                        keep = True # keep all if config empty
                elif current_month in FILTER_CONFIG:
                        req = FILTER_CONFIG[current_month]
                        if req == 'all' or week_counter in req:
                                keep = True

                if keep:
                        cols_to_keep.append(col_name)
                        # match weight index
                        w = raw_weights[weight_index] if weight_index < len(raw_weights) else 0
                        weights_to_use.append(w)
                        used_weeks_map[f"{current_month}_w{week_counter}"] = w

        total_weight = sum(weights_to_use)
        print(f" - columns used: {len(cols_to_keep)} | total sample size: {total_weight}")   
        
        ### calculate wtd-rf
        
        # ensure numeric
        df[cols_to_keep] = df[cols_to_keep].apply(pd.to_numeric, errors='coerce').fillna(0)

        # the math
        weighted_sum = (df[cols_to_keep] * weights_to_use).sum(axis=1)
        df['wtd-rf'] = weighted_sum / total_weight if total_weight > 0 else 0   
        
        ### calculate rank, rfpc
        
        final = df[['Species', 'wtd-rf']].sort_values(by='wtd-rf', ascending=False).reset_index(drop=True)
        final['Rank'] = final.index + 1

        top_score = final['wtd-rf'].iloc[0] if not final.empty else 1
        final['rfpc'] = (final['wtd-rf'] / top_score) * 100     
        
        ### save output
        
        # pull info for filenames
        loc_id = re.search(r'L\d+', filename).group(0)
        loc_name = get_location_name(loc_id)

        # parse date range from filename (YYYY_YYYY_M_M)
        dates = re.search(r'(\d{4})_(\d{4})_(\d)_(\d)', filename)
        date_str = ""
        if dates:
                date_str = f"_{dates.group(1)[-2:]}-{dates.group(2)[-2:]}_{dates.group(3)}-{dates.group(4)}"

        slug = fix_filename_string(loc_name)

        # save in the out dir
        out_csv = os.path.join(OUTPUT_DIR, f"rank_data_{slug}{date_str}.csv")
        out_txt = os.path.join(OUTPUT_DIR, f"summary_{slug}{date_str}.txt")

        final = final[['Rank', 'Species', 'wtd-rf', 'rfpc']]
        final.to_csv(out_csv, index=False)

        create_summary(out_txt, filename, total_weight, final, used_weeks_map, loc_name)
        print(f" - saved: {out_csv}")

def process_data(raw_tsv, loc_id, start_year, end_year):
        print(f"processing data for {loc_id}...")
        f_stream = io.StringIO(raw_tsv)
        lines = f_stream.readlines()
##### run script

if __name__ == "__main__":
        print("starting ranker...")

        # make sure output dir exists
        if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)
                print(f"created output directory: {OUTPUT_DIR}")

        # find text files in the input directory
        if not os.path.exists(INPUT_DIR):
                print(f"error: {INPUT_DIR} does not exist.")
        else:
                files = [f for f in os.listdir(INPUT_DIR) if f.startswith('ebird_') and f.endswith('.txt')]

                if not files:
                        print(f"no files found in {INPUT_DIR}")
        
                for f in files:
                        full_path = os.path.join(INPUT_DIR, f)
                        process_file(full_path, f)

        print("done.")