from sqlalchemy import Column, Integer, TEXT, Float, DateTime, PrimaryKeyConstraint
from datetime import datetime
from app.database import Base

class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True, autoincrement=True,index=True)
    zone = Column(TEXT, index=True)
    telemetry_name = Column(TEXT, index=True)
    value = Column(Float)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, primary_key=True)

    __table_args__ = (
    PrimaryKeyConstraint('id', 'timestamp'),
)