from fastapi import APIRouter, HTTPException
from playwright.async_api import async_playwright
from services.bird_metadata import get_species_image_url


router = APIRouter(
    prefix="/species",
    tags=["Species"]
)


@router.get("/image/{bird_code}")
async def get_bird_image(bird_code: str):
    """
    fetch image URL for a specific bird code.
    added in case we want to fetch images on-demand for specific birds.
    
    args:
        bird_code: eBird bird code (ex. 'amecro' for American Crow)
    
    returns:
        json with bird_code and imageUrl
    """
    
    from services.job_queue import job_manager, JobType
    from fastapi.responses import JSONResponse

    job_id = await job_manager.enqueue_job(
        JobType.FETCH_IMAGE,
        bird_code=bird_code
    )
    
    return JSONResponse(
        status_code=202,
        content={
            "jobId": job_id,
            "status": "queued",
            "message": "Image fetch enqueued. Poll /jobs/{jobId} for results."
        }
    )
