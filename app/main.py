from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.expenses import router as expenses_router
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Au démarrage
    yield
    # À l'arrêt
    engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv("CORS_ORIGINS","").split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expenses_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


