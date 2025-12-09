from services.ranking_engine.data_processing import  get_rankings
import pandas as pd
import os,httpx
from datetime import datetime, timedelta, date
import asyncio, json
import sqlite3

HEADERS = {"X-eBirdApiToken":os.getenv("EBIRD_API_KEY")}
#limit concurrent API calls to prevent exceeding rate limits
SEMAPHORE = asyncio.Semaphore(5)

'''
Provides detailed hotspot overview with optional month/week filtering.

Returns:
-hotspot id,name,region,location, and list of ranked birds for the given hotspot using ranking engine
'''

async def detailed_hotspot_data(
    hotspotID: str,
    start_yr: int | None = None,
    end_yr: int | None = None,
    start_month: int | None = None,
    start_week: int | None = None,
    end_month: int | None = None,
    end_week: int | None = None
):
    ret = await get_rankings(
        hotspotID,
        start_yr,
        end_yr,
        start_month=start_month,
        start_week=start_week,
        end_month=end_month,
        end_week=end_week
    )

    # if ret:
    #     ret = ret['data']
    # else:
    #     return None

    try:
        with sqlite3.connect('server/data/database/locations.db') as sqlConn:
                cursor = sqlConn.cursor()
    
        sql_q = "SELECT ID, NAME, COUNTRY, SUBREGION1, SUBREGION2 FROM 'hotspots' WHERE ID = ?"

        cursor.execute(sql_q, (hotspotID,))

        hotspot_data = cursor.fetchone()

        ranked = None

        ranked = {
        "id": hotspot_data[0],
        "name" : hotspot_data[1],
        "country" : hotspot_data[2],
        "subregion1" :hotspot_data[3],
        "subregion2": hotspot_data[4],
        "birds":ret
        }            

        return ranked

    except sqlite3.Error as e:
        print(f"Database retrieval for detailed hotspot overview failed: {e}")
        return(None)

    finally:
        if sqlConn:
            sqlConn.close()
            print("SQLite connection closed")

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
    #TODO refactor to pull from db
    # loading hotspot specific info
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
            
    try:
        with sqlite3.connect('server/data/database/locations.db') as sqlConn:
                cursor = sqlConn.cursor()
    
        sql_q = '''INSERT INTO 'hotspots' (ID, NAME, COUNTRY, SUBREGION1, SUBREGION2, SPECIESCOUNT) VALUES (?, ?, ?, ?, ?, ?) 
        ON CONFLICT(ID) DO UPDATE SET SPECIESCOUNT = excluded.SPECIESCOUNT 
        WHERE hotspots.SPECIESCOUNT != excluded.SPECIESCOUNT 
        '''

        for hotspot in all_results:
             cursor.execute(sql_q, (hotspot['id'],hotspot['name'],hotspot['country'],hotspot['subregion1'],hotspot['subregion2'],hotspot['speciesCount']))

        return {"status" : f"Saved {len(all_results)} hotspots."}
         

    except sqlite3.Error as e:
        print(f"Database UPDATE failed: {e}")
        return(None)

    finally:
        if sqlConn:
            sqlConn.close()
            print("SQLite connection closed")

def get_overviews(limit:int = 20, offset:int = 0):
    try:
        with sqlite3.connect('server/data/database/locations.db') as sqlConn:
                cursor = sqlConn.cursor()

        sql_q = "SELECT * FROM 'hotspots' ORDER BY SPECIESCOUNT DESC LIMIT ? OFFSET ?"

        print("here")

        cursor.execute(sql_q, (limit, offset))

        hotspot_data = cursor.fetchall()

        overviews = []

        for hotspot in hotspot_data:
            overviews.append({
            "id": hotspot[0],
            "name" : hotspot[1],
            "country" : hotspot[2],
            "subregion1" :hotspot[3],
            "subregion2": hotspot[4],
            "speciesCount":hotspot[5]
            })    

        return overviews
        

    except sqlite3.Error as e:
        print(f"Database overviews retrieval failed: {e}")
        return(None)

    finally:
        if sqlConn:
            sqlConn.close()
            print("SQLite connection closed")
