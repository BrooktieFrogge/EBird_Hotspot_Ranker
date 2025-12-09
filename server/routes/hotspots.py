from fastapi import APIRouter, HTTPException, Path, Query
from services.search_db import dynamic_search
from services.fetch_hotspots import (detailed_hotspot_data,get_location_hotspots,get_overviews)
from models.hotspot_models import (HotspotOverview,DetailedHotspot)
from datetime import datetime
import json
from  typing import Annotated, List

'''
Backend router for retrieving eBird hotspot data.
'''
router = APIRouter(
    prefix="/hotspots",
    tags=["Hotspots"]
    )

'''
Dynamically search by location name (country, subnational, hotspot name)
based on query parameter mode

modes(defaults to None):
    hotspot: returns hotspot overviews for hotspots that match the query. Works with, without, or with only some location filters applied.

    If country,subregion1, or subregion2 are specified they should be exact location names -assumes these values are filters that are already applied, only expects raw user input for hotspot name

    country: returns list of country names that match the query (for filtering)  - expects raw user input for country only (disregards other params)

    subregion1: returns list of subregion1 names that match the query (for filtering)  - expects raw user input for subregion1 and takes exact country name as filter  (disregards other params)

    subregion2: returns list of subregion1 names that match the query (for filtering) - expects raw user input for subregion2 and takes exact subregion1 name as filter (disregards other params)


- Exception: Raises 404 with message.

'''
@router.get("/search")
async def location_search(hotspot:str = '',
                    country:str = '',
                    subregion1:str = '',
                    subregion2:str = '', mode:str = None):
    
    data = dynamic_search(hotspot,country,subregion1,subregion2,mode)

    if not data:
        raise HTTPException(status_code=404, detail="Location not found.")
    return {"results" : data}

'''
Will eventually be background script that updates hotspot overview data monthly
TODO add background scheduler and test refactor
'''
# @router.get("/fetch-hotspot-data")
# async def fetch_hotspot_data():
#     data = await get_location_hotspots()
    
#     if not data:
#         raise HTTPException(status_code=404, detail="Location not found.")
#     return data

'''
Default: returns the first 100 hotspots overviews 
Custom Query: return the number of hotspots specified by the limit starting from the offset
    limit- adjusts the amount of hotspots returned
    offset- adjusts how many overviews to skip from the start of the data set

   TODO add back to Query ,le=len(data)

'''
@router.get("/browse-hotspots", response_model=List[HotspotOverview])
async def browse_hotspots(
    limit:Annotated[
        int|None, 
        Query(description="Amount of overviews to return",ge=0,le=100)]=20,
    offset: Annotated[
        int|None,
          Query(description="Amount of overviews to skip from start of dataset",ge=0)]= 0
    ):

    data = get_overviews(limit,offset)

    if not data:
        raise HTTPException(status_code=404, detail="No Hotspots Found.")
    try:
        return  data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Input: {e}")

'''
Provides detailed hotspot overview with optional month/week filtering.

Returns:
-hotspot id,name,region,location, and list of ranked birds for the given hotspot
'''
@router.get("/report/{hotspotId}", response_model=DetailedHotspot)
async def get_detailed_hotspot_data(
    hotspotId: str,
    start_yr: int | None = Query(None, description="Start year for data range"),
    end_yr: int | None = Query(None, description="End year for data range"),
    start_month: int | None = Query(None, ge=1, le=12, description="Start month (1-12)"),
    start_week: int | None = Query(None, ge=1, le=4, description="Start week within start_month (1-4)"),
    end_month: int | None = Query(None, ge=1, le=12, description="End month (1-12)"),
    end_week: int | None = Query(None, ge=1, le=4, description="End week within end_month (1-4)"),
):
    print(f"Received request for hotspotID: {hotspotId}")
    if end_yr or start_yr:
        if not end_yr or not start_yr:
            raise HTTPException(status_code=400, detail="Invalid Year Input")
        if end_yr < start_yr or end_yr > datetime.now().year:
            raise HTTPException(status_code=400, detail="Invalid Year Input")
        
    data = await detailed_hotspot_data(
        hotspotId,
        start_yr,
        end_yr,
        start_month=start_month,
        start_week=start_week,
        end_month=end_month,
        end_week=end_week
    )
    if not data:
        raise HTTPException(status_code=404, detail="No Information Found.")
    return data


