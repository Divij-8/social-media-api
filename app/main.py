from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from app.database import create_db_and_tables
from app.routers import auth, users, posts, vote, follow

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Startup: Creating tables...")
    create_db_and_tables()
    logger.info("Application started successfully")
    yield
    logger.info("Shutdown: Cleaning up...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Welcome to my Social Media API! Deployed via Render."}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(vote.router)
app.include_router(follow.router)


