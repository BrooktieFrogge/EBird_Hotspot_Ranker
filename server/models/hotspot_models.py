from pydantic import BaseModel
from typing import List, Optional

    
class HotspotOverview(BaseModel):
    id: str
    name: str
    country: str
    subregion1: Optional[str] = None
    subregion2: Optional[str] = None
    speciesCount: int # Found @ "species list for a region" under "product"


class Bird(BaseModel):
    Rank: int
    Species: str
    wtd_rf: float
    rfpc: float
    # photo: str #TODO make seperate endpoint for this? only needed for top N birds 

class DetailedHotspot(BaseModel):
    id: str
    name: str
    country: str
    subregion1: Optional[str] = None
    subregion2: Optional[str] = None
    birds:List[Bird]#list of bird species with data
