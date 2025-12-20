from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
import os
from services.ranking_engine.data_processing import  get_rankings
from models.request_models import RankingFilterRequest
from services.job_queue import job_manager, JobType

'''
Backend router for retrieving eBird hotspot ranking data.
'''
router = APIRouter(
    prefix="/hotspots",
    tags=["Hotspots"]
    )

SESSION_FILE = os.getenv('SESSION_FILE')
    
@router.get('/ranking/{loc}')
async def fetch_ranking_data(
    loc: str,
    filters: RankingFilterRequest = Depends()
):
    """
    get ranked bird species for a location with optional month/week filtering.
    
    example: /ranking/L901084?start_month=5&start_week=1&end_month=9&end_week=2
    (gets birds for May week 1 through September week 2)
    """
    try:
        filters.validate_years()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    job_id = await job_manager.enqueue_job(
        JobType.FETCH_BARCHARTS,
        loc=loc,
        start_yr=filters.start_yr,
        end_yr=filters.end_yr,
        start_month=filters.start_month,
        start_week=filters.start_week,
        end_month=filters.end_month,
        end_week=filters.end_week
    )
    
    return JSONResponse(
        status_code=202,
        content={
            "jobId": job_id,
            "status": "queued",
            "message": "Ranking request enqueued. Poll /jobs/{jobId} for results."
        }
    )