from fastapi import APIRouter, HTTPException, Query, Depends
import os
from services.ranking_engine.data_processing import  get_rankings
from models.ranking_models import FilterConfig
from models.request_models import RankingFilterRequest
'''
Backend router for retrieving eBird hotspot ranking data.
'''
router = APIRouter(
    prefix="/hotspots",
    tags=["Hotspots"]
    )

SESSION_FILE = os.getenv('SESSION_FILE')
    
@router.get('/ranking/{loc}')
def fetch_ranking_data(
    loc: str,
    filters: RankingFilterRequest = Depends()
):
    """
    Get ranked bird species for a location with optional month/week filtering.
    
    Example: /ranking/L901084?start_month=5&start_week=1&end_month=9&end_week=2
    (Gets birds for May week 1 through September week 2)
    """
    try:
        filters.validate_years()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data = get_rankings(
        loc,
        filters.start_yr,
        filters.end_yr,
        start_month=filters.start_month,
        start_week=filters.start_week,
        end_month=filters.end_month,
        end_week=filters.end_week
    )
    if not data:
        raise HTTPException(status_code=404, detail="[error] | Something went wrong. Either bad location ID or invalid cookies.")
    return {"Results" : data}