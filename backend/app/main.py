from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.db.session import Base, engine
from app.routes.ai_summary import router as ai_summary_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="UWD Converter API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(ai_summary_router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "UWD Converter API"}
