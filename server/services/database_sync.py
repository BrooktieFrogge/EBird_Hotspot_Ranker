import pandas as pd
import sqlite3
import os,httpx,asyncio
from services.search_db import normalize

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
            "country": h['countryCode'],
            "subregion1":  h['subnational1Code'] if 'subnational1Code' in h else None,
            "subregion2": h['subnational2Code'] if 'subnational2Code' in h else None,
            "speciesCount": h['numSpeciesAllTime'] if 'numSpeciesAllTime' in h else 0
        } for h in data] #list of hotspots in country

    except Exception as e:
        print(f" [Database Sync] | Exception : {e}")
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
            print(" [Database Sync] | Fetching:", country,end="\n")
            hotspots = await fetch_country_hotspots(client,country)
            all_results.extend(hotspots)
            
    try:

        with sqlite3.connect('server/data/database/locations.db', timeout=60) as sqlConn:
                cursor = sqlConn.cursor()

        sqlConn.execute("PRAGMA journal_mode=WAL")
        sqlConn.execute("BEGIN IMMEDIATE")
  
        #create a updates staging table
        cursor.execute("DROP TABLE IF EXISTS new_hotspots")


        cursor.execute("CREATE TABLE new_hotspots (id TEXT PRIMARY KEY, name TEXT, country_code TEXT, subnational1_code TEXT,  subnational2_code TEXT, species_count INTEGER, norm_name TEXT) ")

        cursor.execute("INSERT INTO new_hotspots (id, name, country_code ,subnational1_code, subnational2_code , species_count, norm_name) SELECT * FROM hotspots ")

        #make updates in staging table        
        sql_q = '''INSERT INTO 'new_hotspots' (id, name, country_code, subnational1_code, subnational2_code, species_count, norm_name) VALUES (?, ?, ?, ?, ?, ?, ?) 

        ON CONFLICT(id) DO UPDATE SET species_count = excluded.species_count 
        WHERE new_hotspots.species_count != excluded.species_count 
        '''

        for hotspot in all_results:
             cursor.execute(sql_q, (hotspot['id'],hotspot['name'],hotspot['country'],hotspot['subregion1'],hotspot['subregion2'],hotspot['speciesCount'], normalize(hotspot['name'])))

        #validate update
        df = pd.read_sql_query('''SELECT * FROM 'hotspots' ''', sqlConn)

        print(f"[Database Sync] |  Old Hotspot overview data. Length: {len(df)}, Head: \n {df.head}")

        df2 = pd.read_sql_query('''SELECT * FROM 'new_hotspots' ''', sqlConn)

        print(f"[Database Sync] | New Hotspot overview data. Length: {len(df2)}, Head: \n {df2.head}")

        old_count = cursor.execute("SELECT COUNT(*) FROM 'hotspots' ").fetchone()[0]

        new_count = cursor.execute("SELECT COUNT(*) FROM 'new_hotspots' ").fetchone()[0]

        if new_count < old_count:
             raise ValueError(f" [ERROR] Table size decreased : Old Size = {old_count} New Size = {new_count}")
        
        #if all is good then swap 
        cursor.execute("ALTER TABLE 'hotspots' RENAME TO old_hotspots")
        cursor.execute("ALTER TABLE 'new_hotspots' RENAME TO hotspots ")
        cursor.execute("DROP TABLE 'old_hotspots' ")
        

        print("[Database Sync] | Database was successfuly updated! Sync Complete.")

        #only commit if everything succedes
        sqlConn.commit()
        return {"status" : f"Saved {len(all_results)} hotspots."}
         

    except sqlite3.Error as e:
        print(f" [Database Sync] | Database UPDATE failed: {e}")
        sqlConn.rollback() # return database to state before update
        return(None)

    finally:
        if sqlConn:
            sqlConn.close()
            print(" [Database Sync] | SQLite connection closed")

