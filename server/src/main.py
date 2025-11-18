from fastapi import FastAPI
from dotenv import load_dotenv
import os,httpx
from datetime import datetime, timedelta, date

load_dotenv()
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "backend api is online. (:"}


'''
Returns info for the given hotspot for a given date range. 
If no range is given default to returning info for entire range of dates available (1800-present).

Values for Testing: 

L1150539 -hotspotID
2017-06-01 - start date
2017-08-30 - end date
'''
@app.get("/hotspot")
async def get_hotspot_obs(hotspotID:str, startDate:str = None,endDate:str = None):
    headers = {"X-eBirdApiToken":os.getenv("EBIRD_API_KEY")}

    if startDate and endDate:
        return await get_dateRange_obs(hotspotID,startDate, endDate)
    else:
        return await get_dateRange_obs(hotspotID,"1800-01-01", date.today())

@app.get("/hotspot/daterange")
async def get_dateRange_obs(hotspotID,startDate,endDate):
    headers = {"X-eBirdApiToken":os.getenv("EBIRD_API_KEY")}
    results = []

    sd = datetime.strptime(startDate,"%Y-%m-%d").date()
    ed = datetime.strptime(endDate,"%Y-%m-%d").date()

    async with httpx.AsyncClient() as client:
        while sd <= ed:
            year,month,day = sd.year,sd.month,sd.day
            url = f"https://api.ebird.org/v2/data/obs/{hotspotID}/historic/{year}/{month}/{day}"

            response = await client.get(url, headers=headers)
            response.raise_for_status()

            formatted = response.json()
            results.extend(formatted)
            sd += timedelta(days=1)

    return {'hotspot data' : results}

# async def get_top_birds(numBirds:int):