from fastapi import APIRouter, HTTPException
from services.hotspot_search import search_hotspots
from services.fetch_hotspots import (get_location_hotspots,detailed_hotspot_data)
from models.hotspot_models import (HotspotOverview,DetailedHotspot)
from typing import Union
from datetime import datetime


'''
Backend router for retrieving eBird hotspot data.
'''
router = APIRouter(
    prefix="/hotspots",
    tags=["Hotspots"]
    )

'''
Dynamically search by location name (country, subnational, hotspot name) or exact hotspot id when querying with Id_lookup=True

Returns:
- Default: Returns a list of locations that represent possible matches to the query. List contatins dictionary for each location contatining location name and code (for broader regions) or hotspot name and hotspot id

- Id_lookup: Returns the name of the hotspot.

- Exception: Raises 404 with message.

'''
@router.get("/search/location/{query}")
async def location_search(query: str, Id_lookup: bool | None = None):
    data = search_hotspots(query,Id_lookup)
    if not data:
        raise HTTPException(status_code=404, detail="Location not found.")
    return {"results" : data}

'''
Get the hotspots in a region given the location code (country,subnational)

Returns: A list of hotspots in the given region. Each hotspot is represented with a dictionary containing the hotspots metadata.
'''
# @router.get("/browse/{location_code}")
# async def location_hotspots_search(location_code:str):
#     data = get_location_hotspots(location_code)
#     if not data:
#         raise HTTPException(status_code=404, detail="No Hotspots Found.")
#     return {"results" : data}


@router.get("/browse-hotspots", response_model=HotspotOverview)
async def browse_hotspots():
    data = await get_location_hotspots()
    if not data:
        raise HTTPException(status_code=404, detail="No Hotspots Found.")
    return data

'''
Provides standard or detailed hotspot overview (is detailed=True). 

Returns:
-Standard: Returns id,name,region,location, and species count for the given hotspot

-Detailed: Returns id,name,region, location, and list of ranked birds for the given hotspot

'''
@router.get("/report/{hotspotID}/", response_model=DetailedHotspot)
def get_detailed_hotspot_data(hotspotId:str, start_yr: int |None = None, end_yr: int |None = None):
    if end_yr or start_yr:
        if not end_yr or not start_yr:
            raise HTTPException(status_code=400, detail="Invalid Year Input")
        if end_yr < start_yr or end_yr > datetime.now().year:
            raise HTTPException(status_code=400, detail="Invalid Year Input")
    data =  detailed_hotspot_data(hotspotId, start_yr,end_yr)
    if not data:
        raise HTTPException(status_code=404, detail="No Information Found.")
    return data


