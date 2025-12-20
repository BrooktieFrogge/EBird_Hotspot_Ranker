from fastapi import APIRouter, HTTPException
from services.job_queue import job_manager

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.get("/{job_id}")
async def get_job_status(job_id: str):
    # get current status of job
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
