from pydantic import BaseModel
from typing import List

    
class HotspotModel(BaseModel):
    id: str
    name: str
    country: str
    subregion1: str
    subregion2:str
    speciesCount: int # Found @ "species list for a region" under "product"

class HotspotOverview(BaseModel):
    List[HotspotModel]

class Bird(BaseModel):
    Rank: int
    Species: str
    wtd_rf: float
    rfpc: float
    # photo: str #TODO make seperate endpoint for this? only needed for top 3 birds 

class DetailedHotspot(BaseModel):
    id: str
    name: str
    region: str
    location: str 
    birds:List[Bird]#list of bird species with data
