from fastapi import FastAPI
from dotenv import load_dotenv
import os,httpx
from datetime import datetime, timedelta, date
import asyncio

'''
Backend API for retrieving eBird hotspot oservations over a date range.
'''
#load environment variables and initialize app
load_dotenv()
app = FastAPI()

#limit concurrent API calls to prevent exceeding rate limits
SEMAPHORE = asyncio.Semaphore(5)

"""
Root endpoint
"""
@app.get("/")
def read_root():
    return {"message": "backend api is online. (:"}

'''
Returns eBird hotspot checklist info for a given daterange

If no date range is provided => default to the entire dataset (1900-present)

Example Args: 

L1150539 -hotspotID (required)
2017-06-01 - start date
2017-08-30 - end date

Returns: dictionary of checklist data for the specified hotspot
'''

@app.get("/get-hotspots-info")
async def get_hotspot_checklists(
        hotspotID:str,
        startDate:str |None = None,
        endDate:str | None = None
        ):
    #if user provies valid date range then use it to fetch
    if startDate and endDate and endDate >= startDate:
        return await get_dateRange(hotspotID,startDate, endDate)
    
    #otherwise get default range (based off eBird barchart data)
    default_start = "1900-01-01"
    default_end = date.today().strftime("%Y-%m-%d")

    return await get_dateRange(hotspotID,default_start,default_end)

'''
Fetch observations for a single day.

- handles 429/503 rate limit errors using exponential backoff
- response filtering 
- concurrency limiting using sempahore

Returns: list of filterd checklist dictionaries including 'locId','subId','speciesCode', and 'comName'
'''
async def fetch_days(client,hotspotID:str,d:date, attempt=1):
    headers = {"X-eBirdApiToken":os.getenv("EBIRD_API_KEY")}

    #protect external API from overload
    async with SEMAPHORE:

        url = f"https://api.ebird.org/v2/data/obs/{hotspotID}/historic/{d.year}/{d.month}/{d.day}?hotspot=true&detail=full"

        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            #small delay to workaround limits
            await asyncio.sleep(0.25)        
            data = response.json()

            #if no sightings that day then the data is empty list
            if not isinstance(data,list):
                return []
        
            #columns to keep, shorten responses before appending
            filterby =  ['locId','subId','speciesCode','comName']

            filtered = []

            for entry in data:
                filtered_entry = {key: entry[key] for key in filterby if key in entry}
                if filtered_entry:
                    filtered.append(filtered_entry)

            return filtered
        
        #if rate limited retry
        except httpx.HTTPStatusError as e:
            #handle overload with exponential backoff
            if e.response.status_code in (429,503) and attempt < 3:
                await asyncio.sleep(2 ** attempt)
                return await fetch_days(client,hotspotID,d,attempt+1)
            return []
        
        except Exception:
            return []

'''
Fetch checklists for a range of dates.

Returns: dictionary of flattened list of checklist info for hotspot
'''
async def get_dateRange(hotspotID:str,startDate:str,endDate:str):
    #convert strings to date objects
    sd = datetime.strptime(startDate,"%Y-%m-%d").date()
    ed = datetime.strptime(endDate,"%Y-%m-%d").date()

    #generate lists of all days in range
    dates = []
    while sd<=ed:
        dates.append(sd)
        sd += timedelta(days=1)

    #fetch all days concurrently and gather results
    async with httpx.AsyncClient() as client:
        tasks = [fetch_days(client,hotspotID,d) for d in dates]    

        results = await asyncio.gather(*tasks)

    #flatten list of lists
    flattened_results = [item for daily in results for item in daily]

    return {"hotspot data": flattened_results}