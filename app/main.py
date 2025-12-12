from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: Creating tables...")
    create_db_and_tables()
    yield
    print("Shutdown: Cleaning up...")


app = FastAPI(lifespan=lifespan)

