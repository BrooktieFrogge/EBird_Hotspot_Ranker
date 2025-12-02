from pydantic import BaseModel
from typing import List,Dict

class FilterConfig(BaseModel):
    weeks: Dict[ str , List[int] ]
