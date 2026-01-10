from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine, Base
from .routers import owners, pets
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(title="Pet Service", version="1.0.0", lifespan=lifespan)

app.include_router(owners.router)
app.include_router(pets.router)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Pet Service API"}