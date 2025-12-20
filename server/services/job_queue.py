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
        self.worker_tasks = []
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

    # background cleanup task
    async def _cleanup_loop(self):
        print("[JobQueue] Cleanup task started")
        while self.running:
            try:
                await asyncio.sleep(3600)  # run every hour
                now = datetime.now()
                # remove jobs older than 1 hour
                expired_ids = []
                for jid, job in self.jobs.items():
                    # check age
                    created = datetime.fromisoformat(job["created_at"]) 
                    age = (now - created).total_seconds()
                    
                    # keep jobs for 1 hour for polling
                    if age > 3600 and job["status"] in [JobStatus.COMPLETED, JobStatus.FAILED]:
                        expired_ids.append(jid)
                
                for jid in expired_ids:
                    del self.jobs[jid]
                
                if expired_ids:
                    print(f"[JobQueue] Cleaned up {len(expired_ids)} expired jobs")

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[JobQueue] cleanup error: {e}")

    # start background workers
    async def start_worker(self):
        if self.running:
            return
        self.running = True
        # 40 workers (adjusted for small mem)
        self.worker_tasks = [
            asyncio.create_task(self._worker_loop(i)) for i in range(40)
        ]
        # add cleanup task
        self.worker_tasks.append(asyncio.create_task(self._cleanup_loop()))
        print(f"[JobQueue] {len(self.worker_tasks)} workers started (inc. cleanup)")


    # stop background workers
    async def stop_worker(self):
        self.running = False
        if self.worker_tasks:
            for task in self.worker_tasks:
                task.cancel()
            
            await asyncio.gather(*self.worker_tasks, return_exceptions=True)
            self.worker_tasks = []
            
        print("[JobQueue] all workers stopped")

    # background loop processing jobs
    async def _worker_loop(self, worker_id: int):
        print(f"[JobQueue] worker {worker_id} loop running")
        while self.running:
            try:
                job_id = await self.queue.get()
                
                # kill any job taking too long
                try:
                    await asyncio.wait_for(self._process_job(job_id), timeout=300)
                except asyncio.TimeoutError:
                    print(f"[JobQueue] job {job_id} TIMED OUT (Fail-Safe Triggered). Killing worker.")
                    # manually mark as failed
                    job = self.jobs.get(job_id)
                    if job:
                        job["status"] = JobStatus.FAILED
                        job["error"] = "Server Busy: Job timed out (Limit: 300s)"
                        job["updated_at"] = datetime.now().isoformat()
                        
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

        job["status"] = JobStatus.PROCESSING
        job["updated_at"] = datetime.now().isoformat()
        
        try:
            # get shared browser instance
            # serialized access via worker loop
            browser = await get_browser()
            payload = job["payload"]
            
            result = None
            
            if job["type"] == JobType.FETCH_BARCHARTS:
                from services.ranking_engine.fetch_barcharts import ensure_session
                from services.ranking_engine.data_processing import get_rankings
                
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