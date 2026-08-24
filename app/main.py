from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.expenses import router as expenses_router
from app.database import Base, engine
from app import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Au démarrage
#    Base.metadata.create_all(bind=engine)
    yield
    # À l'arrêt
    engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(expenses_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


