from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.expenses import router as expenses_router
from app.database import Base, engine
from app import models
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Au démarrage
#    Base.metadata.create_all(bind=engine)
    yield
    # À l'arrêt
    engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://127.0.0.1:5500",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expenses_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


