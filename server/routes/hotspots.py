from fastapi import APIRouter, HTTPException, Path, Query
from services.hotspot_search import search_hotspots
from services.fetch_hotspots import (detailed_hotspot_data)
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

with open('server/data/hotspot-overviews.json','r') as file:
        data = json.load(file)

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
Default: returns the first 100 hotspots overviews 
Custom Query: return the number of hotspots specified by the limit starting from the offset
    limit- adjusts the amount of hotspots returned
    offset- adjusts how many overviews to skip from the start of the data set
'''
@router.get("/browse-hotspots/{limit}", response_model=List[HotspotOverview])
async def browse_hotspots(
    limit:Annotated[
        int, 
        Path(description="Amount of overviews to return",ge=0,le=100)],
    offset: Annotated[
        int|None,
          Query(description="Amount of overviews to skip from start of dataset",ge=0,le=len(data))]= 0
    ):

    if not data:
        raise HTTPException(status_code=404, detail="No Hotspots Found.")
    try:
        return  data[offset:(offset+limit+1)]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Input: {e}")

'''
Provides detailed hotspot overview with optional month/week filtering.

Returns:
-hotspot id,name,region,location, and list of ranked birds for the given hotspot
'''
@router.get("/report/{hotspotId}", response_model=DetailedHotspot)
def get_detailed_hotspot_data(
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
        
    data = detailed_hotspot_data(
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


