from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from routes import hotspots, rankings, species


from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apscheduler.triggers.cron import CronTrigger
from services.database_sync import sync_data
from services.browser_manager import close_browser
import os
from contextlib import asynccontextmanager
from datetime import datetime

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start scheduler on app startup
    scheduler = AsyncIOScheduler()
    trigger = CronTrigger(
        day=int((os.getenv("DATA_SYNC_DAY"))), 
        hour=int((os.getenv("DATA_SYNC_HOUR"))))

    job = scheduler.add_job(sync_data, trigger=trigger )

    if os.getenv("MANUAL_SYNC") == "True":
        job.modify(next_run_time=datetime.now())


    scheduler.start()
    print("[Background Data Sync] | Waiting for trigger")

    # start job queue worker
    from services.job_queue import job_manager
    await job_manager.start_worker()

    yield

    # cleanup on shutdown
    await job_manager.stop_worker()
    scheduler.shutdown()
    await close_browser()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hotspots.router)
app.include_router(species.router)
from routes import jobs
app.include_router(jobs.router)

@app.get("/")
def main():
    # health check

    return {"message": "backend online"}
