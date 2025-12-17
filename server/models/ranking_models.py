from pydantic import BaseModel
from typing import List, Dict, Optional
from models.species_models import Bird

class DetailedHotspot(BaseModel):
    id: str
    name: str
    country: str
    subregion1: Optional[str] = None
    subregion2: Optional[str] = None
    total_sample_size: float
    sample_sizes_by_week: dict[str, float]
    birds:List[Bird]#list of bird species with data
