from rapidfuzz import process, fuzz
import pandas as pd
import unicodedata
import re

'''
API for dynamically searching eBird hotspot locations using rapidfuzz matching.

This feature works by loading three CSV datasets and a custom JSON file containing region and hotspot specific information, normalizing the names to remove accents and special characters to produce autocomplete/correction matching using Levenshtein Distance, and exposing two  API endpoints for searching by name or hotspot location id.
'''

#DATA LOADING=======================================================
countryInfo = pd.read_csv('server/data/countries-Table 1.csv')
sub1Info = pd.read_csv('server/data/subnational1 regions-Table 1.csv')
sub2Info = pd.read_csv('server/data/subnational2 regions-Table 1.csv')

#loading hotspot specific info
hotspotInfo = pd.read_json('server/data/hotspot_names_and_IDs.json')
       
#combine name columns into one series
locationNames = pd.concat([hotspotInfo['locName'],countryInfo['country_name'],sub1Info['subnational1_name'],sub2Info['subnational2_name']],ignore_index=True)

#combine the region codes columns in the same order
locationCodes = pd.concat([hotspotInfo['countryCode'],countryInfo['country_code'],sub1Info['subnational1_code'],sub2Info['subnational2_code']],ignore_index=True)

#add the loc id columns for hotspots
hotspotIds = pd.concat([hotspotInfo['locId'],pd.Series([None]* (len(locationNames) - len(hotspotInfo)))],ignore_index=True)

#add the subnat1 codes columns for hotspots
hotspotSubCodes = pd.concat([hotspotInfo['subnational1Code'],pd.Series([None]* (len(locationNames) - len(hotspotInfo)))],ignore_index=True)

#create a LOCATIONS of locations names and ids for easy lookup
LOCATIONS = pd.DataFrame({'LocName':locationNames,'LocCode':locationCodes,'HotspotId':hotspotIds, "HotspotSubCode":hotspotSubCodes})

'''
Normalize text by removing accents, converting to basic ASCII characters, lowercasing, and triming whitespace

Returns: Normalized string for rapidfuzz matching
'''
def normalize(text:str):
     lower_c  = text.lower()
     no_accents  = unicodedata.normalize('NFKD', lower_c).encode('ascii','ignore').decode()
     no_punct = re.sub(r'[^\w\s]',' ',no_accents)
     return no_punct

'''
loc_name: exact location name (country/subnational)
Returns:
-List of dicts with hotspot info that are in that region
-None if no location found
-Message if location given is a hotspot.
'''
def get_location_hotspots(loc_name: str, loc_code:str):
    condition1 = LOCATIONS['LocName'] == loc_name
    condition2 = LOCATIONS['LocCode'] == loc_code

    #find row with exact name
    row = LOCATIONS.loc[condition1&condition2]
    
    if row.empty:
        return None # location not found in df
    
    row = row.iloc[0]
    
    # case A: row is a hotspot
    if row['HotspotId'] != None:
        return "[Location given was a Hotspot. Enter Exact Country or Subnational Name for Results]"
    #case B: row is not a hotspot - find all hotspots with the same location  code
    loc_hotspots = LOCATIONS.loc[
            (LOCATIONS['LocCode'] == loc_code)|(LOCATIONS['HotspotSubCode'] == loc_code) & (LOCATIONS['HotspotId'].notna()),['LocName','HotspotId','HotspotSubCode']
        ]
    
    #make results pretty
    hotspots_list = (loc_hotspots.rename(columns={'LocName': 'Hotspot Name','HotspotId': 'Hotspot Id','HotspotSubCode': 'Hotspot SubNatonal1 Code'})).to_dict(orient='records')

    if not hotspots_list[0]['Hotspot Id']: #if no hotspots found
        return False
    
    return hotspots_list # can be an empty list if not hotspots found

"""
query : user serach input (text or exact hotspot id)

id_lookup : if True, treat query as hotspot id (locId)

Returns: list, string, or None
- if query is an id lookup : return name of hotspot of None if not found
- if query is name search: return a list of dicts including fuzzy matched REGIONS and hotspots (including hotspot ids) 
"""
def search_hotspots(query:str, id_lookup: bool  = False, limit:int = 10):
    results = []

    # id look up - return exact hotspot name
    if id_lookup:
        row = LOCATIONS.loc[LOCATIONS['HotspotId'] == query]
        if row.empty:
            return None
        return row.iloc[0]['LocName']
    
    # normalize query 
    norm_query = normalize(query)

    # make  normalized version of dataset for matching
    LOCATIONS['NormName'] = LOCATIONS['LocName'].apply(normalize)
    # extract the top rapidfuzz matches (# specified by optional limit parameter)
    fuzzy_matches = process.extract(norm_query,LOCATIONS['NormName'].to_dict().values(), scorer=fuzz.ratio, limit=limit) # use dict to get index values

    if not fuzzy_matches:
        return None

    # process each match
    ## match normalized names back to original names and ids
    for match, score, idx in fuzzy_matches:
        row = LOCATIONS.iloc[idx] # get original row
       
        hotspot_id = row['HotspotId']

        # case A: this row is a hotspot, append the name and id
        if pd.notna(hotspot_id):
            loc_name = row['LocName']
            results.append({"hotspot name": loc_name, "hotspot id": hotspot_id})
            continue

        loc_name = row['LocName']
        loc_code = row['LocCode']
        #case B: not a hotspot, append name and loc code
        results.append({"location name" : loc_name, "location code" : loc_code})

    return results 

