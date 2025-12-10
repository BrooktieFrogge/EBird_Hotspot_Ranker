import pandas as pd
import sqlite3
import os,httpx,asyncio

HEADERS = {"X-eBirdApiToken":os.getenv("EBIRD_API_KEY")}

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
            "country": get_cname(h['countryCode']),
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
async def sync_data():
 
    print("[Background Data Sync] | Database sync started...")

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
        #TODO update with real database path for production

        with sqlite3.connect('server/data/database/COPY.db') as sqlConn:
                cursor = sqlConn.cursor()

        sql_q = '''INSERT INTO 'hotspots' (ID, NAME, COUNTRY, SUBREGION1, SUBREGION2, SPECIESCOUNT) VALUES (?, ?, ?, ?, ?, ?) 
        ON CONFLICT(ID) DO UPDATE SET SPECIESCOUNT = excluded.SPECIESCOUNT 
        WHERE hotspots.SPECIESCOUNT != excluded.SPECIESCOUNT 
        '''

        for hotspot in all_results:
             cursor.execute(sql_q, (hotspot['id'],hotspot['name'],hotspot['country'],hotspot['subregion1'],hotspot['subregion2'],hotspot['speciesCount']))
        
        df = pd.read_sql_query('''SELECT * FROM 'hotspots' ''', sqlConn)

        print(f"Hotspot overview data updated successfully. Length: {len(df)}, Head: \n {df.head}")

        sqlConn.commit()

        print("[Background Data Sync] | Database sync finished")
        return {"status" : f"Saved {len(all_results)} hotspots."}
         

    except sqlite3.Error as e:
        print(f"Database UPDATE failed: {e}")
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
Returns: subregion 2 name given subregion 2 code.
'''
def get_cname(c_code):
    cInfo = pd.read_csv('server/data/countries-Table 1.csv')

    row = cInfo.loc[cInfo['country_code'] == c_code]

    if row.empty:
        return "None"
    return row.iloc[0]['country_name']