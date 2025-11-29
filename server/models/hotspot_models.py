from pydantic import BaseModel
from typing import List

class MetadataRes(BaseModel):
    locId: str
    name: str
    lat: float
    lng: float
    country: str
    subnational1: str
    subnational2: str

class ChecklistRecordRes(BaseModel):
    locId : str
    subId : str
    obsDt : str
    howMany: int = None
    speciesCode : str
    comName : str

class DateRangeRes(BaseModel):
    records: List[ChecklistRecordRes]

class SingleDayRes(BaseModel):
    records : List[ChecklistRecordRes]

class HotspotSearchRes(BaseModel):
    hotspots : List[str]
