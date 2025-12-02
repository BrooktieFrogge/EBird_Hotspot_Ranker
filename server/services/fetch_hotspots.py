from services.ranking_engine.data_processing import  get_rankings

import os,httpx
from datetime import datetime, timedelta, date
import asyncio

HEADERS = {"X-eBirdApiToken":os.getenv("EBIRD_API_KEY")}
#limit concurrent API calls to prevent exceeding rate limits
SEMAPHORE = asyncio.Semaphore(5)

def detailed_hotspot_data(hotspotID: str, start_yr: int |None = None, end_yr: int |None = None, detailed:bool| None = False):

    #if not detailed return count of birds ever seen in loc
    retStr = "speciesCount"
    ret =  location_bird_count(hotspotID)

    #if detailed return a list of ranked birds
    if detailed:
        retStr = "birds"
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

    ret = {
        "id": hotspotID,
        "name" : data["name"],
        "region" : data["countryName"],
        "location" : data["subnational1Name"],
        retStr: ret
    }

    return ret

'''
 Fetches hotspots within a specified country or region.

 Returns: 
'''
def get_location_hotspots(loc_code: str):
    url = f"https://api.ebird.org/v2/ref/hotspot/{loc_code}?fmt=json"

    res = httpx.get(url,headers=HEADERS)
    
    if res.status_code != 200:
        return None
    
    data = res.json()

    return data

'''
 Fetches a list of species codes for species ever seen in a region, in taxonomic order (species taxa only)

 Returns: Count of birds ever seen in region 
'''
def location_bird_count(loc_id: str):
    url = f"https://api.ebird.org/v2/product/spplist/{loc_id}"

    res = httpx.get(url,headers=HEADERS)

    if res.status_code != 200:
        return None
    
    data = res.json()
    
    return len(data)


