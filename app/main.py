from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_db_and_tables
from app.models import UserRead
from app.routers import auth, users, posts, vote, follow

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: Creating tables...")
    create_db_and_tables()
    yield
    print("Shutdown: Cleaning up...")

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(vote.router)
app.include_router(follow.router)


