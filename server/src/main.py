from fastapi import FastAPI
from dotenv import load_dotenv
import os,httpx
from datetime import datetime, timedelta, date
import asyncio

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

    if startDate and endDate and endDate >= startDate:
        return await get_dateRange_obs(hotspotID,startDate, endDate)
    else:
        default_end = date.today()

        default_start = (default_end - timedelta(days=))
        return await get_dateRange_obs(hotspotID,"1800-01-01", date.today().strftime("%Y-%m-%d"))

'''
Fetch observations for a single day
'''
async def fetch_days(hotspotID:str,d:date):
    headers = {"X-eBirdApiToken":os.getenv("EBIRD_API_KEY")}

    year,month,day = d.year,d.month,d.day
    url = f"https://api.ebird.org/v2/data/obs/{hotspotID}/historic/{year}/{month}/{day}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
       
        
        

async def get_dateRange_obs(hotspotID,startDate,endDate):

    sd = datetime.strptime(startDate,"%Y-%m-%d").date()
    ed = datetime.strptime(endDate,"%Y-%m-%d").date()

    dates = []
    while sd<=ed:
        dates.append(sd)
        sd += timedelta(days=1)

    all_dates = [fetch_days(hotspotID,d) for d in dates]
    
    #Use asyncio.gather to run the tass concurrently and gather their results
    results = await asyncio.gather(*all_dates)

    #flatten list of lists
    flattened_results = [item for sub in results if sub for item in sub]

    return {"hotspot data": flattened_results}
 
# async def get_top_birds(numBirds:int):