import asyncio
import uuid
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
from services.browser_manager import get_browser

'''
manages a single-worker queue to serialize playwright usage.

job lifecycle:
    1. route enqueues job -> receives job_id
    2. worker processes job (one at a time)
    3. client polls /jobs/{job_id} for completion
'''
# job types
class JobType(str, Enum):
    FETCH_BARCHARTS = "FETCH_BARCHARTS"
    GENERATE_PDF = "GENERATE_PDF"
    FETCH_IMAGE = "FETCH_IMAGE"
    FETCH_HOTSPOT_REPORT = "FETCH_HOTSPOT_REPORT"

# job status
class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobManager:
    # initialize queue
    def __init__(self):
        self.queue = asyncio.Queue()
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.worker_task = None
        self.running = False

    # enqueue job and return id
    async def enqueue_job(self, job_type: JobType, **payload) -> str:
        job_id = str(uuid.uuid4())
        job = {
            "id": job_id,
            "type": job_type,
            "status": JobStatus.QUEUED,
            "payload": payload,
            "result": None,
            "error": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.jobs[job_id] = job
        await self.queue.put(job_id)
        print(f"[JobQueue] Enqueued job {job_id} ({job_type})")
        return job_id

    # get job by id
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self.jobs.get(job_id)

    # start background worker
    async def start_worker(self):
        if self.running:
            return
        self.running = True
        self.worker_task = asyncio.create_task(self._worker_loop())
        print("[JobQueue] worker started")

    # stop background worker
    async def stop_worker(self):
        self.running = False
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass
        print("[JobQueue] worker stopped")

    # background loop processing jobs
    async def _worker_loop(self):
        print("[JobQueue] worker loop runnning")
        while self.running:
            try:
                job_id = await self.queue.get()
                await self._process_job(job_id)
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[JobQueue] worker error: {e}")
                await asyncio.sleep(1)

    # execute single job logic
    async def _process_job(self, job_id: str):
        job = self.jobs.get(job_id)
        if not job:
            return

        print(f"[JobQueue] processing job {job_id}...")
        job["status"] = JobStatus.PROCESSING
        job["updated_at"] = datetime.now().isoformat()
        
        try:
            # get shared browser instance
            # serialized access via worker loop
            browser = await get_browser()
            
            result = None
            
            if job["type"] == JobType.FETCH_BARCHARTS:
                from services.ranking_engine.fetch_barcharts import ensure_session
                from services.ranking_engine.data_processing import get_rankings
                
                payload = job["payload"]
                loc = payload["loc"]
                
                await ensure_session(browser)
                
                result = await get_rankings(
                    loc,
                    payload.get("start_yr"),
                    payload.get("end_yr"),
                    start_month=payload.get("start_month"),
                    start_week=payload.get("start_week"),
                    end_month=payload.get("end_month"),
                    end_week=payload.get("end_week"),
                    cached_raw_data=payload.get("cached_raw_data")
                )

            elif job["type"] == JobType.FETCH_HOTSPOT_REPORT:
                from services.fetch_hotspots import detailed_hotspot_data
                
                result = await detailed_hotspot_data(
                    hotspotID=payload["hotspot_id"],
                    start_yr=payload.get("start_yr"),
                    end_yr=payload.get("end_yr"),
                    start_month=payload.get("start_month"),
                    start_week=payload.get("start_week"),
                    end_month=payload.get("end_month"),
                    end_week=payload.get("end_week")
                )
                
            elif job["type"] == JobType.GENERATE_PDF:
                from services.pdf_export import generate_pdf
                result_bytes = await generate_pdf(**job["payload"])
                
                # encode bytes to base64 string for json
                import base64
                if result_bytes:
                    result = base64.b64encode(result_bytes).decode('utf-8')
                else:
                    raise Exception("pdf generation returned no data")
                
            elif job["type"] == JobType.FETCH_IMAGE:
                from services.bird_metadata import get_species_image_url
                bird_code = job["payload"]["bird_code"]
                
                page = await browser.new_page()
                try:
                    result = await get_species_image_url(bird_code, browser_page=page)
                finally:
                    await page.close()

            job["result"] = result
            job["status"] = JobStatus.COMPLETED
            print(f"[JobQueue] job {job_id} completed")
            
        except Exception as e:
            print(f"[JobQueue] job {job_id} failed: {e}")
            job["error"] = str(e)
            job["status"] = JobStatus.FAILED
        finally:
            job["updated_at"] = datetime.now().isoformat()

job_manager = JobManager()