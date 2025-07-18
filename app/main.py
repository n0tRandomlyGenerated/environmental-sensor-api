from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.api_routes import router
from app.routes.auth_routes import auth_router
from app.database import engine, Base
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
import time
from fastapi.staticfiles import StaticFiles

def wait_for_db():
    from app.database import engine
    retries = 0
    while True:
        try:
            conn = engine.connect()
            conn.close()
            print("✅ DB connection established")
            break
        except OperationalError:
            print("⚠️ Waiting for DB to become available...")
            retries += 1
            if retries > 15:
                raise Exception("❌ Could not connect to DB after 15 retries")
            time.sleep(2)

def setup_timescaleDB():
    with engine.connect() as conn:
        print("🧾 Lifespan startup: Creating hypertable...")
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb;"))
        conn.execute(text("SELECT create_hypertable('sensor_data', 'timestamp', if_not_exists => true, migrate_data => true);"))
        conn.execute(text("COMMIT;"))
    print("✅ DB and TimescaleDB ready")


Base.metadata.create_all(bind=engine)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ Starting up...")
    wait_for_db()
    setup_timescaleDB()
    yield 
    print("👋 Shutting down...")

app = FastAPI(title="Environmental Sensor API")
app.include_router(router, prefix="/api", tags=["API"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.mount("/", StaticFiles(directory="static", html=True), name="static")