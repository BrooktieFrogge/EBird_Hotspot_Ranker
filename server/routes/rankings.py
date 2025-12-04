from fastapi import APIRouter, HTTPException, Query
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
    
@router.get('/ranking/{loc}')
def fetch_ranking_data(
    loc: str,
    start_yr: int | None = Query(None, description="Start year for data range"),
    end_yr: int | None = Query(None, description="End year for data range"),
    start_month: int | None = Query(None, ge=1, le=12, description="Start month (1-12)"),
    start_week: int | None = Query(None, ge=1, le=4, description="Start week within start_month (1-4)"),
    end_month: int | None = Query(None, ge=1, le=12, description="End month (1-12)"),
    end_week: int | None = Query(None, ge=1, le=4, description="End week within end_month (1-4)"),
):
    """
    Get ranked bird species for a location with optional month/week filtering.
    
    Example: /ranking/L901084?start_month=5&start_week=1&end_month=9&end_week=2
    (Gets birds for May week 1 through September week 2)
    """
    data = get_rankings(
        loc,
        start_yr,
        end_yr,
        start_month=start_month,
        start_week=start_week,
        end_month=end_month,
        end_week=end_week
    )
    if not data:
        raise HTTPException(status_code=404, detail="[error] | Something went wrong. Either bad location ID or invalid cookies.")
    return {"Results" : data}