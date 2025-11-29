from fastapi import APIRouter, HTTPException, Query
from services.hotspot_search import search_hotspots
from server.services.fetch_hotspots import (get_single_day,get_dateRange,get_recent_checklists,get_metadata)

from models.hotspot_models import (MetadataRes,DateRangeRes,SingleDayRes)

'''
Backend router for retrieving eBird hotspot checklist data.
'''

router = APIRouter(
    prefix="/hotspots",
    tags=["Hotspots"]
    )

@router.get("search/{query}")
async def location_search(query: str, iD: bool | None = None):
    data = search_hotspots(query,iD)
    if not data:
        raise HTTPException(status_code=404, detail="Hotspot not found.")
    return {"hotspots" : data}

@router.get("/{locId}/data", response_model = MetadataRes)
async def hotspot_metadata(locId:str):
    data = await get_metadata(locId)
    if not data:
        raise HTTPException(status_code=404, detail="Hotspot not found.")
    return data

@router.get("/{locId}/recent", response_model = DateRangeRes)
async def hotspot_recent_records(locId:str):
    data = await get_recent_checklists(locId)
    if not data:
        raise HTTPException(status_code=404, detail="Hotspot not found.")
    return {"records": data}

@router.get("/{locId}/{start}/{end}/records", response_model = DateRangeRes)
async def hotspot_daterange_records(locId:str,start:str,end:str):
    data = await get_dateRange(locId,start,end)
    if not data:
        raise HTTPException(status_code=404, detail="Invalid Request.")
    return {"records": data}

@router.get("/{locId}/{date}/records", response_model = SingleDayRes)
async def hotspot_single_day_records(locId:str,date:str):
    data = await get_single_day(locId,date)
    if not data:
        raise HTTPException(status_code=404, detail="Invalid Request.")
    return {"records": data}



