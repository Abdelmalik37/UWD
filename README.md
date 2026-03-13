# UWD - Wearable Data to FHIR Platform

Wearable data ingestion platform that parses uploaded files and converts extracted metrics into HL7 FHIR resources.

## Features
- Upload any wearable data file (JSON, CSV, XML, TCX, GPX)
- Parse raw data and extract health metrics
- Convert to HL7 FHIR JSON (Patient, Device, Observation, Bundle)
- Store original file, parsed raw data, FHIR output, and metadata
- Simple dashboard and upload history UI

## Project Structure
- `backend/` FastAPI + parsing + FHIR mapper
- `frontend/` React dashboard
- `datasets/` sample files (TCX, GPX, CSV, JSON, XML)

## FHIR Output (Example)
FHIR output is a `Bundle` containing `Patient`, `Device`, and one or more `Observation` resources.

## Local Run (without Docker)
### Backend
```powershell
cd backend
python -m pip install fastapi uvicorn python-multipart pydantic-settings sqlalchemy
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend
```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Open: `http://127.0.0.1:5173`

## Run on another device (same Wi-Fi)
1. Find host IP:
```powershell
ipconfig
```
2. Start backend on all interfaces:
```powershell
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
3. Set frontend API base:
Create `frontend/.env`:
```env
VITE_API_BASE_URL=http://YOUR_HOST_IP:8000
```
4. Start frontend on all interfaces:
```powershell
cd frontend
npm run dev -- --host 0.0.0.0 --port 5173
```
5. Open from another device:
`http://YOUR_HOST_IP:5173`

## API Endpoints
- `POST /upload`
- `GET /upload/{id}`
- `POST /convert/{id}`
- `GET /fhir/{id}`
- `GET /uploads`

## Database Schema
Uploads table stores:
- Original file (base64)
- Parsed raw data (JSON)
- FHIR resources (JSON)
- Upload metadata

## Sample Files
Use files in `datasets/`:
- `apple_health_sample.xml`
- `sample_activity.tcx`
- `sample_route.gpx`
- `garmin_sample.csv`
- `fitbit_api_response.json`

## Notes
- If PostgreSQL is unavailable, backend falls back to SQLite (`uwd_local.db`).
- Parsing supports JSON, CSV, XML. TCX/GPX are treated as XML.
