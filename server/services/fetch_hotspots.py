from services.ranking_engine.data_processing import  get_rankings
import pandas as pd
import os,httpx
from datetime import datetime, timedelta, date
import asyncio, json

HEADERS = {"X-eBirdApiToken":os.getenv("EBIRD_API_KEY")}
#limit concurrent API calls to prevent exceeding rate limits
SEMAPHORE = asyncio.Semaphore(5)

'''
Provides detailed hotspot overview with optional month/week filtering.

Returns:
-hotspot id,name,region,location, and list of ranked birds for the given hotspot using ranking engine
'''

def detailed_hotspot_data(
    hotspotID: str,
    start_yr: int | None = None,
    end_yr: int | None = None,
    start_month: int | None = None,
    start_week: int | None = None,
    end_month: int | None = None,
    end_week: int | None = None
):
    
    ret = get_rankings(
        hotspotID,
        start_yr,
        end_yr,
        start_month=start_month,
        start_week=start_week,
        end_month=end_month,
        end_week=end_week
    )

    if ret:
        ret = ret['data']
    else:
        return None

    with open('server/data/hotspot-overviews.json','r')as file:
        hotspot_data = json.load(file)

    ranked = None

    for hotspot in hotspot_data:

        if hotspot['id'] == hotspotID:
            ranked = {
            "id": hotspot['id'],
            "name" : hotspot['name'],
            "country" : hotspot['country'],
            "subregion1" :hotspot['subregion1'],
            "subregion2": hotspot['subregion1'],
            "birds":ret
            }            
            break

    return ranked

'''
Returns: subregion 1 name given subregion 1 code.
'''
def get_subregion1(sub_code):
    sub1Info = pd.read_csv('server/data/subnational1 regions-Table 1.csv')

    row = sub1Info.loc[sub1Info['subnational1_code'] == sub_code]
    if row.empty:
        return "None"
    return row.iloc[0]['subnational1_name']

'''
Returns: subregion 2 name given subregion 2 code.
'''
def get_subregion2(sub_code):
    sub2Info = pd.read_csv('server/data/subnational2 regions-Table 1.csv')

    row = sub2Info.loc[sub2Info['subnational2_code'] == sub_code]

    if row.empty:
        return "None"
    return row.iloc[0]['subnational2_name']
    
'''
Fetches all hotspot overview info for a country.

Returns:  list of dicts with filtered hotspots data
'''
async def fetch_country_hotspots(client,country_code):
    url =f"https://api.ebird.org/v2/ref/hotspot/{country_code}?fmt=json"

    try:
        res = await client.get(url,headers=HEADERS,timeout=20)
        res.raise_for_status()

        await asyncio.sleep(0.25)
        
        data = res.json()

        filtered = [{
            "id": h['locId'],
            "name": h['locName'],
            "country": h['countryCode'],
            "subregion1":  get_subregion1(h['subnational1Code']) if 'subnational1Code' in h else None,
            "subregion2":  get_subregion2(h['subnational2Code']) if 'subnational2Code' in h else None,
            "speciesCount": h['numSpeciesAllTime'] if 'numSpeciesAllTime' in h else 0
        } for h in data] #list of hotspots in country

    except Exception as e:
        print(f"exception {e}")
        return None

    return filtered

'''
Uses ebird api calls to fetch most recent hotspot info for all locations by country

Returns: list of dictionaries containing info about each hotspot. Dumps information into a json file.
'''
async def get_location_hotspots():
    #loading hotspot specific info
    df = pd.read_csv('server/data/countries-Table 1.csv')
    country_codes = df['country_code'].to_list()

    all_results = []

    async with httpx.AsyncClient() as client:
        for country in country_codes:
            if pd.isna(country):
                continue
            print("Fetching:", country,end="\n")
            hotspots = await fetch_country_hotspots(client,country)
            all_results.extend(hotspots)

    with open('hotspot-overviews.json','w') as f:
        json.dump(all_results,f,indent=4)

    print(f"Saved {len(all_results)} hotspots.")

    return all_results
