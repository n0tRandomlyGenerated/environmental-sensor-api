# Environmental Sensor API

A modern, containerized backend system for ingesting, storing, and visualizing environmental sensor data. Built with FastAPI, PostgreSQL with TimescaleDB, and Docker Compose, this project demonstrates clean architecture, time-series optimization, secure API access, and test-driven development.

---

## 🚀 Project Overview

This backend service is designed to collect and serve environmental sensor readings (e.g., temperature, humidity, pressure) from multiple zones. Key capabilities include:

- Ingesting real-time sensor data via a REST API
- Storing data efficiently using TimescaleDB (optimized for time-series)
- Exposing summarized and bucketed data for analysis or visualization
- Enforcing API key-based access control
- Optional Grafana dashboard for live data exploration
- Fully tested with `pytest` and Dockerized for portability

---

## 🛠️ Technologies Used

- **FastAPI** – High-performance async API framework
- **PostgreSQL + TimescaleDB** – Time-series optimized relational database
- **SQLAlchemy 2.0** – ORM for DB interactions
- **Docker Compose** – Container orchestration for app + DB + Grafana
- **Grafana** – Optional frontend for sensor visualization
- **Pytest** – Test suite with coverage for core functionality
- **Pydantic** – Data validation and serialization
- **Lifespan events** – Clean, modern FastAPI startup/shutdown handling

---

## 📁 Folder Structure

```
.
├── app/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── config.py                # App settings and environment loading
│   ├── database.py              # SQLAlchemy DB connection setup
│   ├── models.py                # ORM models
│   ├── schemas.py               # Pydantic schemas
│   ├── crud.py                  # DB access logic
│   ├── dependencies.py          # API key verification, shared logic
│   └── routes/
│       └── sensor_routes.py     # API route handlers
├── tests/
│   └── test_api.py              # Pytest test cases
├── dashboards/
│   └── Environmental_Sensor_Dashboard.json  # Grafana export
├── requirements.txt             # Python dependencies
├── Dockerfile                   # FastAPI app container
└── docker-compose.yml           # Orchestration config
```

---

## 🧪 How to Run & Test

### Prerequisites

- Docker + Docker Compose
- Python 3.11 (for running tests locally)

### Start the Application

```bash
docker-compose up --build
```

The following services will start:

- FastAPI app → [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)
- PostgreSQL + TimescaleDB
- Grafana → [http://localhost:3000](http://localhost:3000)

> You can use Swagger UI to test endpoints, generate an API key, and seed the database from available endpoints.

### Run Tests

```bash
docker exec -it <app_container> pytest
```

Or locally (if DB is accessible):

```bash
pytest -v --capture=tee-sys
```

---

## 📡 API Endpoints

### 🔐 Authentication

All endpoints (except `/auth/generate-api-key`) require a valid API key passed in the header:

```
X-API-Key: your_key_here
```

---

### 🔑 Generate API Key

```
GET /auth/generate-api-key
```

Returns a temporary API key for testing.  
Available in Swagger UI under **auth** section:  
➡️ [http://localhost:8000/docs#/auth](http://localhost:8000/docs#/auth)

---

### 🧪 Seed Database (Optional)

```
POST /seed_db
```

Seeds the database with sample sensor data for development and testing.  
Available in Swagger UI under **sensor_routes** section.

---

### 📥 Ingest Data

```
POST /api/data
```

Ingest a sensor reading.

**Payload:**

```json
{
  "zone": "ZoneA",
  "telemetry_name": "temperature",
  "value": 23.5,
  "timestamp": "2025-07-18T10:00:00Z"
}
```

---

### 📤 Retrieve Data

```
GET /api/data?zone=ZoneA&telemetry_name=temperature
```

Query sensor data with optional filters.

---

### 📊 Summary Statistics

```
GET /api/summary?zone=ZoneA&telemetry_name=humidity&start=...&end=...
```

Returns min, max, and average for a sensor in a time range.

---

### 📈 Time-Bucketed Summary

```
GET /api/summary/bucketed?zone=ZoneA&telemetry_name=humidity&bucket_size=1 hour
```

Returns time-series summaries using TimescaleDB’s `time_bucket()` function.

---

## 📺 Grafana Dashboard

- **Access:** [http://localhost:3000](http://localhost:3000)
- **Login:** Default user/pass is `admin / admin`
- **Import dashboard:** Use `dashboards/Environmental_Sensor_Dashboard.json`

The dashboard includes:

- Time series per metric per zone
- Reading count trends
- Zone-level comparison heatmaps
- Bucketed averages over time

> Tip: Use `/seed_db` to populate data for visualization testing.

---

## ✅ Test Suite

Implemented using **pytest** and covers:

- Valid sensor reading ingestion
- GET filtering and summaries
- API key requirement and rejection
- Invalid time range handling
- Error handling: 404s and validation errors

**Test cases include:**

- `test_post_data`
- `test_get_all_data`
- `test_get_summary_bucketed`
- `test_api_key_required`
- `test_api_key_invalid`
- `test_summary_bucketed_invalid_time_range`
- `test_404_on_invalid_route`
- `test_post_data_missing_field`

---

## 🔐 API Key Validation

API keys are managed internally via:

- A temporary key generated via `/auth/generate-api-key`
- Checked using FastAPI dependencies
- Verified via `X-API-Key` header
- Response: `403 Forbidden` if missing/invalid

---

## 🧵 Background Tasks

The app uses FastAPI’s `BackgroundTasks` for:

- Non-blocking log persistence
- Deferred operations that shouldn't slow down API responses

---
