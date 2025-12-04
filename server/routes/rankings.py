from fastapi import APIRouter, HTTPException
import os
from services.ranking_engine.data_processing import  get_rankings
from models.ranking_models import FilterConfig
'''
Backend router for retrieving eBird hotspot ranking data.
'''
router = APIRouter(
    prefix="/hotspots",
    tags=["Hotspots"]
    )

SESSION_FILE = os.getenv('SESSION_FILE')

### TODO: add option to input # weeks 
    
@router.get('/ranking/{loc}/{start}/{end}')
def fetch_ranking_data(loc: str, start_yr: str | None = None, end_yr:str | None = None):
    data = get_rankings(loc,start_yr,end_yr)
    if not data:
        raise HTTPException(status_code=404, detail="[error] | Something went wrong. Either bad location ID or invalid cookies.")
    return {"Results" : data}