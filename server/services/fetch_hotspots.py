from services.ranking_engine.data_processing import  get_rankings
import pandas as pd
import os
import asyncio
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

    if ret:
        ret = ret['data']
    else:
        return None

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
