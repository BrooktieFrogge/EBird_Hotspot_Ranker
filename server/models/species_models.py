from pydantic import BaseModel
from typing import List, Optional

class Bird(BaseModel):
    Rank: int
    Species: str
    wtd_rf: float
    rfpc: float
    birdCode: Optional[str] = None
    speciesUrl: Optional[str] = None
    imageUrl: Optional[str] = None
