from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import StreamingResponse
from services.search_db import dynamic_search
from services.fetch_hotspots import (detailed_hotspot_data,get_overviews)
from services.database_sync import sync_data
from services.database_sync import sync_data
from services.pdf_export import generate_pdf
from models.hotspot_models import HotspotOverview
from models.ranking_models import DetailedHotspot
from models.request_models import HotspotSearchRequest, HotspotBrowseRequest, RankingFilterRequest
from datetime import datetime
import json
import os
import io
from  typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, Query, Depends

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

mode(defaults to hotspot):
    hotspot: returns hotspot overviews for hotspots that match the query. Works with, without, or with only some location filters applied.

    If country,subregion1, or subregion2 are specified they should be exact location names -assumes these values are filters that are already applied, only expects raw user input for hotspot name

    country: returns list of country names that match the query (for filtering)  - expects raw user input for country only (disregards other params)

    subregion1: returns list of subregion1 names that match the query (for filtering)  - expects raw user input for subregion1 and takes exact country name as filter  (disregards other params)

    subregion2: returns list of subregion1 names that match the query (for filtering) - expects raw user input for subregion2 and takes exact subregion1 name as filter (disregards other params)


- Exception: Raises 404 with message.

'''
@router.get("/search")
async def location_search(request: HotspotSearchRequest = Depends()):
    
    data = dynamic_search(request.hotspot, request.country, request.subregion1, request.subregion2, request.mode, request.limit)

    if not data:
        raise HTTPException(status_code=404, detail="Location not found.")
    return {"results" : data}

'''
Will eventually be background script that updates hotspot overview data monthly
TODO add background scheduler and test refactor
'''
@router.get("/fetch-hotspot-data")
async def fetch_hotspot_data():
    data = await sync_data()
    
    if not data:
        raise HTTPException(status_code=404, detail="Location not found.")
    return data

'''
Default: returns the first 100 hotspots overviews 
Custom Query: return the number of hotspots specified by the limit starting from the offset
    limit- adjusts the amount of hotspots returned
    offset- adjusts how many overviews to skip from the start of the data set

   TODO add back to Query ,le=len(data)

'''
@router.get("/browse-hotspots", response_model=List[HotspotOverview])
async def browse_hotspots(
    request: HotspotBrowseRequest = Depends()
    ):

    data = get_overviews(request.limit, request.offset)

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
    filters: RankingFilterRequest = Depends()
):
    print(f"Received request for hotspotID: {hotspotId}")
    try:
        filters.validate_years()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    data = await detailed_hotspot_data(
        hotspotId,
        filters.start_yr,
        filters.end_yr,
        start_month=filters.start_month,
        start_week=filters.start_week,
        end_month=filters.end_month,
        end_week=filters.end_week
    )
    if not data:
        raise HTTPException(status_code=404, detail="No Information Found.")
    return data


'''
generates a pdf of the hotspot report using playwright.
opens the printable report view and captures it as pdf.
'''
@router.get("/report/{hotspotId}/pdf")
async def get_report_pdf(
    hotspotId: str,
    filters: RankingFilterRequest = Depends(),
    num_top_birds: int = Query(10, ge=1, le=500),
    show_graph: bool = Query(True),
    show_photos: bool = Query(True),
    custom_ranks: str = Query(None),
    photo_ranks: str = Query(None),
    gen_date: str = Query(None),
):
    # get the client URL from environment, default to localhost
    client_url = os.getenv("CLIENT_URL", "http://localhost:5173")
    
    try:
        pdf_bytes = await generate_pdf(
            client_url=client_url,
            hotspot_id=hotspotId,
            num_top_birds=num_top_birds,
            show_graph=show_graph,
            show_photos=show_photos,
            start_year=filters.start_yr,
            end_year=filters.end_yr,
            start_month=filters.start_month,
            start_week=filters.start_week,
            end_month=filters.end_month,
            end_week=filters.end_week,
            custom_ranks=custom_ranks,
            photo_ranks=photo_ranks,
            gen_date=gen_date,
        )
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=hotspot_report_{hotspotId}.pdf"
            }
        )
    except Exception as e:
        print(f"[error] | PDF generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

