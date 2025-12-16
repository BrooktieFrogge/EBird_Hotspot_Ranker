from pydantic import BaseModel
from typing import List, Optional

    
class HotspotOverview(BaseModel):
    id: str
    name: str
    country: str
    subregion1: Optional[str] = None
    subregion2: Optional[str] = None
    speciesCount: int # Found @ "species list for a region" under "product"