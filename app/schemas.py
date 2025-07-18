from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SensorDataCreate(BaseModel):
    zone: str
    telemetry_name: str
    value: float
    timestamp: Optional[datetime] = None

class SensorDataOut(SensorDataCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class SummaryResponse(BaseModel):
    zone: str
    telemetry_name: str
    min: float
    max: float
    avg: float
    from_ts: datetime
    to_ts: datetime

class BucketedSummaryResponse(BaseModel):
    bucket: datetime
    min: float
    max: float
    avg: float

class MessageResponse(BaseModel):
    message: str