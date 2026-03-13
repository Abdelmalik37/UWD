# UWD Quick Start (FHIR)

## Backend
```powershell
cd C:\Users\Wad Yonis\Desktop\UWD\backend
python -m pip install fastapi uvicorn python-multipart pydantic-settings sqlalchemy
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Frontend
```powershell
cd C:\Users\Wad Yonis\Desktop\UWD\frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Open: `http://127.0.0.1:5173`

## Cross-device (same Wi-Fi)
```powershell
ipconfig
```
Create `C:\Users\Wad Yonis\Desktop\UWD\frontend\.env`:
```env
VITE_API_BASE_URL=http://YOUR_HOST_IP:8000
```
Then:
```powershell
cd C:\Users\Wad Yonis\Desktop\UWD\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
cd C:\Users\Wad Yonis\Desktop\UWD\frontend
npm run dev -- --host 0.0.0.0 --port 5173
```
Open: `http://YOUR_HOST_IP:5173`
