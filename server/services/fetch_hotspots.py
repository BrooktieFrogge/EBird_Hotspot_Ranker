from services.ranking_engine.data_processing import  get_rankings
import pandas as pd
import os,httpx
from datetime import datetime, timedelta, date
import asyncio

HEADERS = {"X-eBirdApiToken":os.getenv("EBIRD_API_KEY")}
#limit concurrent API calls to prevent exceeding rate limits
SEMAPHORE = asyncio.Semaphore(5)

def detailed_hotspot_data(hotspotID: str, start_yr: int |None = None, end_yr: int |None = None):
    
    ret = get_rankings(hotspotID,start_yr,end_yr)
    if ret:
        ret = ret['data']
    else:
        return None

    url = f"https://api.ebird.org/v2/ref/hotspot/info/{hotspotID}"

    res = httpx.get(url,headers=HEADERS)
    
    if res.status_code != 200:
        return None
    data = res.json()

    ranked = {
        "id": hotspotID,
        "name" : data["name"],
        "region" : data["countryName"],
        "location" : data["subnational1Name"],
        "birds": ret
    }
    return ranked

'''
 Fetches hotspots within a specified country or region.

 Returns: 
'''
# def get_location_hotspots(loc_code: str):
#     url = f"https://api.ebird.org/v2/ref/hotspot/{loc_code}?fmt=json"

#     res = httpx.get(url,headers=HEADERS)
    
#     if res.status_code != 200:
#         return None
    
#     data = res.json()

#     return data

def get_subregion1(sub_code):
    sub1Info = pd.read_csv('server/data/subnational1 regions-Table 1.csv')

    row = sub1Info.loc[sub1Info['subnational1_code'] == sub_code]
    if row.empty:
        return "None"
    return row.iloc[0]['subnational1_name']

def get_subregion2(sub_code):
    sub2Info = pd.read_csv('server/data/subnational2 regions-Table 1.csv')

    row = sub2Info.loc[sub2Info['subnational2_code'] == sub_code]

    if row.empty:
        return "None"
    return row.iloc[0]['subnational2_name']
    

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

async def get_location_hotspots():
    #loading hotspot specific info
    df = pd.read_csv('server/data/countries-Table 1.csv')
    country_codes = df['country_code'].to_list()

    all_results = []

    async with httpx.AsyncClient() as client:
        for country in country_codes:
            print("Fetching:", country)
            hotspots = await fetch_country_hotspots(client,country)
            all_results.extend(hotspots)

    print(f"Done collecting {len(all_results)} hotspots")
    return all_results



