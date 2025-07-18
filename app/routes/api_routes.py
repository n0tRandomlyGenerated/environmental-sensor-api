from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import SensorDataCreate, SensorDataOut, MessageResponse, BucketedSummaryResponse
from app.crud import add_sensor_data, get_all_data, get_bucketed_summary
from app.database import get_db
from datetime import datetime, timedelta
from app.models import SensorData
from app.dependencies import verify_api_key
import random

router = APIRouter(dependencies=[Depends(verify_api_key)])

@router.post("/data", response_model=SensorDataOut)
def create_data( data: SensorDataCreate, db: Session = Depends(get_db)):
    return add_sensor_data(db, data)

@router.get("/data", response_model=List[SensorDataOut])
def read_data(
    zone: str = None,
    telemetry_name: str = None,
    from_ts: datetime = None,
    to_ts: datetime = None,
    db: Session = Depends(get_db)
):
    return get_all_data(db, zone, telemetry_name, from_ts, to_ts)

@router.get("/summary/bucketed", response_model=list[BucketedSummaryResponse])
def bucketed_summary_data(
    zone: str,
    telemetry_name: str,
    from_ts: datetime,
    to_ts: datetime,
    background_tasks: BackgroundTasks,
    bucket_width: str = "1 hour",
    db: Session = Depends(get_db),
):
    if from_ts > to_ts:
        raise HTTPException(status_code=400, detail="from_ts must be before to_ts")
    background_tasks.add_task(log_summary_request, zone, telemetry_name, from_ts, to_ts, bucket_width)
    return get_bucketed_summary(db, zone, telemetry_name, from_ts, to_ts, bucket_width)

def log_summary_request(zone, name, from_ts, to_ts, bucket_width):
    print(f"🔄 Background: Summary requested for {zone}/{name} from {from_ts} to {to_ts} ({bucket_width})")


@router.post("/seed_db", response_model=MessageResponse)
def seed_database(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    for _ in range(1000):
        data = SensorData(
            zone=random.choice(["ZoneA", "ZoneB", "ZoneC"]),
            telemetry_name=random.choice(["temperature", "humidity", "pressure"]),
            value=round(random.uniform(20, 40), 2),
            timestamp=now - timedelta(hours=random.randint(0,23),minutes=random.randint(0, 30))
        )
        db.add(data)
    db.commit()
    return {"message": "✅ Seeded 1000 records"}