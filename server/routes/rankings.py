from fastapi import APIRouter, HTTPException, Query
import os
from services.ranking_engine.live_ranker import BROWSER
from services.ranking_engine.fetch_barcharts import fetch_data

'''
Backend router for retrieving eBird hotspot ranking data.
'''
router = APIRouter(
    prefix="/hotspots",
    tags=["Hotspots"]
    )

SESSION_FILE = os.getenv('SESSION_FILE')

### main data request function
        ##need error handling for dates
@router.get('/ranking/{loc}/{start}/{end}')
async def fetch_ranking_data(loc: str, start: str | None = None, end:str | None = None):
    data = fetch_data(loc,start,end)
    if not data:
        raise HTTPException(status_code=404, detail="[error] | something went wrong. either bad location ID or invalid cookies.")
    return {"ranking" : data}