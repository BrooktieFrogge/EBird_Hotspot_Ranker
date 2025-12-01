from fastapi import APIRouter, HTTPException
from services.hotspot_search import search_hotspots, get_location_hotspots
from services.fetch_hotspots import (get_single_day,get_dateRange,get_recent_checklists,get_metadata)

from models.hotspot_models import (MetadataRes,DateRangeRes,SingleDayRes)

'''
Backend router for retrieving eBird hotspot checklist data.
'''

router = APIRouter(
    prefix="/hotspots",
    tags=["Hotspots"]
    )

@router.get("search/location/{query}")
async def location_search(query: str, Id_lookup: bool | None = None):
    data = search_hotspots(query,Id_lookup)
    if not data:
        raise HTTPException(status_code=404, detail="Location not found.")
    return {"results" : data}

@router.get("search/get-location-hotspots/{location_name}/{location_code}")
async def location_hotspots_search(location_name: str,location_code:str):
    data = get_location_hotspots(location_name,location_code)
    if not data:
        raise HTTPException(status_code=404, detail="Hotspot not found.")
    return {"results" : data}

@router.get("/{hotspotId}/data", response_model = MetadataRes)
async def hotspot_metadata(hotspotId:str):
    data = await get_metadata(hotspotId)
    if not data:
        raise HTTPException(status_code=404, detail="Hotspot not found.")
    return data

@router.get("/{hotspotId}/recent", response_model = DateRangeRes)
async def hotspot_recent_records(hotspotId:str):
    data = await get_recent_checklists(hotspotId)
    if not data:
        raise HTTPException(status_code=404, detail="Hotspot not found.")
    return {"records": data}

@router.get("/{hotspotId}/{start}/{end}/records", response_model = DateRangeRes)
async def hotspot_daterange_records(hotspotId:str,start:str,end:str):
    data = await get_dateRange(hotspotId,start,end)
    if not data:
        raise HTTPException(status_code=404, detail="Invalid Request.")
    return {"records": data}

@router.get("/{hotspotId}/{date}/records", response_model = SingleDayRes)
async def hotspot_single_day_records(hotspotId:str,date:str):
    data = await get_single_day(hotspotId,date)
    if not data:
        raise HTTPException(status_code=404, detail="Invalid Request.")
    return {"records": data}



