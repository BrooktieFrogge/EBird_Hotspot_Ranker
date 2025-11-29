from fuzzywuzzy import process
import pandas as pd
import unicodedata
import json
'''
API for dynamically searching eBird hotspot locations using fuzzy matching.

This feature works by loading three CSV datasets containing region specific information, normalizing the names to remove accents and special characters to produce autocomplete/correction matching using Levenshtein Distance, and exposing a single API endpoint for searching by name.
'''


#DATA LOADING=======================================================
countryInfo = pd.read_csv('server/data/countries-Table 1.csv')
sub1Info = pd.read_csv('server/data/subnational1 regions-Table 1.csv')
sub2Info = pd.read_csv('server/data/subnational2 regions-Table 1.csv')

#combine name columns into one series
locationNames = pd.concat([countryInfo['country_name'],sub1Info['subnational1_name'],sub2Info['subnational2_name']],ignore_index=True)

#combine the ID columns in the same order
locationIDs = pd.concat([countryInfo['country_code'],sub1Info['subnational1_code'],sub2Info['subnational2_code']],ignore_index=True)

#create a dataframe of locations names and ids for easy lookup
LOCATIONS = pd.DataFrame({'LocName':locationNames,'LocID':locationIDs})

'''
Normalize text by removing accents and converting to basic ASCII characters

Returns: Normalized string without accents/special characters
'''
def normalize(text:str):
     text  = unicodedata.normalize('NFKD',text)
     text  = ''.join([c for c in text if not unicodedata.combining(c)])
     return text.lower().strip()

"""
Searches the location dataset using fuzzy matching. Endpoint normalizes the user's query, normalizes all location names, and performs fuzzy match to find the top 20 best matches.

Returns: List of dictionaries wiht location Name + ID pairs for the matched rows - takes in either a locId or a locName and return correct info

"""
def search_hotspots(query:str, id = False):
    results = []
    if not id:
        # normalize query 
        query = query.lower().strip()
        
        # make  normalized version of dataset for matching
        normalized_locs = [normalize(name) for name in LOCATIONS['LocName']]

        # extract the top 20 fuzzy wuzzy matches
        fuzzy_matches = process.extract(query, normalized_locs,limit=20)

        #ignore match scores, note: matches are in order of best match score
        matches = [val[0].lower() for val in fuzzy_matches]

        # match normalized names back to original names and ids
        for norm in matches:
            for orig_name,loc_id in zip(LOCATIONS["LocName"],LOCATIONS["LocID"]):
                if normalize(orig_name) == norm:
                    results.append({"name":orig_name, "id":loc_id})
                    break 

        return results
    
    else:
        with open('server/data/hotspot_names_and_IDs.json','r') as f:
            hotspots = json.load(f)

        for h in hotspots:
            if h["locId"] == query:
                return h
    return []

'''
make methods that given the exact region name returns locid, and given list of hotspots in that region - change names to reflect hotspot vs locid vs region search 
'''