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
    birdCode: Optional[str] = None
    speciesUrl: Optional[str] = None
    imageUrl: Optional[str] = None

class DetailedHotspot(BaseModel):
    id: str
    name: str
    country: str
    subregion1: Optional[str] = None
    subregion2: Optional[str] = None
    total_sample_size: float
    sample_sizes_by_week: dict[str, float]
    birds:List[Bird]#list of bird species with data
