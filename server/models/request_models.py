from pydantic import BaseModel
from typing import Optional, Annotated
from fastapi import Query
from datetime import datetime

class HotspotSearchRequest(BaseModel):
    hotspot: str = ''
    country: str = ''
    subregion1: str = ''
    subregion2: str = ''
    mode: str = 'hotspot'
    limit: int = 60

class HotspotBrowseRequest(BaseModel):
    limit: Annotated[int | None, Query(description="Amount of overviews to return", ge=0, le=100)] = 20
    offset: Annotated[int | None, Query(description="Amount of overviews to skip from start of dataset", ge=0)] = 0

class RankingFilterRequest(BaseModel):
    start_yr: int | None = Query(None, description="Start year for data range")
    end_yr: int | None = Query(None, description="End year for data range")
    start_month: int | None = Query(None, ge=1, le=12, description="Start month (1-12)")
    start_week: int | None = Query(None, ge=1, le=4, description="Start week within start_month (1-4)")
    end_month: int | None = Query(None, ge=1, le=12, description="End month (1-12)")
    end_week: int | None = Query(None, ge=1, le=4, description="End week within end_month (1-4)")

    def validate_years(self):
        if self.end_yr or self.start_yr:
            if not self.end_yr or not self.start_yr:
                raise ValueError("Invalid Year Input")
            if self.end_yr < self.start_yr or self.end_yr > datetime.now().year:
                raise ValueError("Invalid Year Input")
