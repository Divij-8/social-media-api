from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from models import UserRead
from routers import auth, users, posts



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


@app.get("/")
def root():
    return {"message": "Welcome!"}