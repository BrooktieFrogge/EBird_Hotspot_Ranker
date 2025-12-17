from services.ranking_engine.data_processing import  get_rankings
import pandas as pd
import os
import asyncio
import sqlite3
from cachetools import TTLCache

HEADERS = {"X-eBirdApiToken":os.getenv("EBIRD_API_KEY")}
#limit concurrent API calls to prevent exceeding rate limits
SEMAPHORE = asyncio.Semaphore(5)

# cache hotspot rankings for 5 minutes to speed up pdf gen
HOTSPOT_CACHE = TTLCache(maxsize=50, ttl=300)

def get_cache_key(hotspotID, start_yr, end_yr, start_month, start_week, end_month, end_week):
    """Generate a unique cache key based on all filter parameters"""
    return f"{hotspotID}:{start_yr}:{end_yr}:{start_month}:{start_week}:{end_month}:{end_week}"

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
    # check cache first
    cache_key = get_cache_key(hotspotID, start_yr, end_yr, start_month, start_week, end_month, end_week)
    if cache_key in HOTSPOT_CACHE:
        print(f"[cache] | HIT for {hotspotID} - using cached data")
        return HOTSPOT_CACHE[cache_key]
    
    print(f"[cache] | MISS for {hotspotID} - fetching from eBird")
    
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
        birds = ret['data']
        total_sample_size = ret['total_sample_size']
        sample_sizes_by_week = ret['sample_sizes_by_week']

    else:
        return None

    try:
        with sqlite3.connect('server/data/database/locations.db') as sqlConn:
                cursor = sqlConn.cursor()
    
        sql_q = "SELECT h.id, h.name, c.country_name, s1.subnational1_name, s2.subnational2_name, h.species_count, h.norm_name FROM 'hotspots' AS h LEFT JOIN 'countries' AS c ON h.country_code = c.country_code LEFT JOIN 'subregions1' AS s1 ON h.subnational1_code = s1.subnational1_code LEFT JOIN 'subregions2' AS s2 ON h.subnational2_code = s2.subnational2_code  WHERE h.id = ?"

        cursor.execute(sql_q, (hotspotID,))

        hotspot_data = cursor.fetchone()

        ranked = None

        ranked = {
        "id": hotspot_data[0],
        "name" : hotspot_data[1],
        "country" : hotspot_data[2],
        "subregion1" :hotspot_data[3],
        "subregion2": hotspot_data[4],
        "total_sample_size": total_sample_size,
        "sample_sizes_by_week": sample_sizes_by_week,
        "birds":birds
        }
        
        # store in cache for pdf gen
        HOTSPOT_CACHE[cache_key] = ranked
        print(f"[cache] | stored {hotspotID} in cache (expires in 5 min)")

        return ranked

    except sqlite3.Error as e:
        print(f" [Database Request] | Database retrieval for detailed hotspot overview failed: {e}")
        return(None)

    finally:
        if sqlConn:
            sqlConn.close()
            print(" [Database Request] | SQLite connection closed")

def get_overviews(limit:int = 20, offset:int = 0):
    try:
        with sqlite3.connect('server/data/database/locations.db') as sqlConn:
                cursor = sqlConn.cursor()

        sql_q = "SELECT h.id, h.name, c.country_name, s1.subnational1_name, s2.subnational2_name, h.species_count, h.norm_name FROM 'hotspots' AS h LEFT JOIN 'countries' AS c ON h.country_code = c.country_code LEFT JOIN 'subregions1' AS s1 ON h.subnational1_code = s1.subnational1_code LEFT JOIN 'subregions2' AS s2 ON h.subnational2_code = s2.subnational2_code ORDER BY h.species_count DESC LIMIT ? OFFSET ?"

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
        print(f" [Database Request] | Database overviews retrieval failed: {e}")
        return(None)

    finally:
        if sqlConn:
            sqlConn.close()
            print(" [Database Request] | SQLite connection closed")
