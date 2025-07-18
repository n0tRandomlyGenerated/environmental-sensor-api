from sqlalchemy.orm import Session
from app.models import SensorData
from app.schemas import SensorDataCreate, BucketedSummaryResponse
from datetime import datetime
from sqlalchemy import func, text
from fastapi import HTTPException

def add_sensor_data(db: Session, data: SensorDataCreate):
    db_data = SensorData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_all_data(db: Session, zone: str = None, name: str = None, from_ts: datetime = None, to_ts: datetime = None):
    query = db.query(SensorData)
    if zone:
        query = query.filter(SensorData.zone == zone)
    if name:
        query = query.filter(SensorData.telemetry_name == name)
    if from_ts:
        query = query.filter(SensorData.timestamp >= from_ts)
    if to_ts:
        query = query.filter(SensorData.timestamp <= to_ts)
    return query.all()

def get_bucketed_summary(db: Session, zone: str, name: str, from_ts: datetime, to_ts: datetime, bucket_width: str = "1 hour"):
    
    ALLOWED_BUCKET_WIDTHS = {"1 minute", "5 minutes", "1 hour", "1 day", "1 week"}

    if bucket_width not in ALLOWED_BUCKET_WIDTHS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid bucket_width. Must be one of {', '.join(ALLOWED_BUCKET_WIDTHS)}"
        )

    query = text(f"""
        SELECT 
            time_bucket('{bucket_width}', timestamp) AS bucket,
            MIN(value) AS min,
            MAX(value) AS max,
            AVG(value) AS avg
        FROM sensor_data
        WHERE 
            zone = :zone AND 
            telemetry_name = :name AND 
            timestamp BETWEEN :from_ts AND :to_ts
        GROUP BY bucket
        ORDER BY bucket
    """)

    result = db.execute(query, {
        "zone": zone,
        "name": name,
        "from_ts": from_ts,
        "to_ts": to_ts,
    }).fetchall()

    return [
        BucketedSummaryResponse(
            bucket=item.bucket,
            min=item.min,
            max=item.max,
            avg=item.avg
        )
        for item in result
    ]