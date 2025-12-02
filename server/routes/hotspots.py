from fastapi import APIRouter, HTTPException
from services.hotspot_search import search_hotspots
from services.fetch_hotspots import (get_location_hotspots,detailed_hotspot_data)
from models.hotspot_models import (HotspotOverview,DetailedHotspot)
from typing import Union

'''
Backend router for retrieving eBird hotspot checklist data.
'''

router = APIRouter(
    prefix="/hotspots",
    tags=["Hotspots"]
    )

@router.get("/search/location/{query}")
async def location_search(query: str, Id_lookup: bool | None = None):
    data = search_hotspots(query,Id_lookup)
    if not data:
        raise HTTPException(status_code=404, detail="Location not found.")
    return {"results" : data}


@router.get("/browse/{location_code}")
async def location_hotspots_search(location_code:str):
    data = await get_location_hotspots(location_code)
    if not data:
        raise HTTPException(status_code=404, detail="No Hotspots Found.")
    return {"results" : data}


@router.get("/report/{hotspotID}/", response_model =Union[DetailedHotspot,HotspotOverview])
def get_detailed_hotspot_data(hotspotId:str, start_yr: int |None = None, end_yr: int |None = None, detailed:bool| None = False):
    data =  detailed_hotspot_data(hotspotId, start_yr,end_yr,detailed)
    if not data:
        raise HTTPException(status_code=404, detail="No Information Found.")
    return data





