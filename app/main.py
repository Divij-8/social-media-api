from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from database import create_db_and_tables, SessionDep
from sqlmodel import Session
from database import get_session
from models import User, UserCreate, UserRead
from app.security import hash_password


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: Creating tables...")
    create_db_and_tables()
    yield
    print("Shutdown: Cleaning up...")


app = FastAPI(lifespan=lifespan)


@app.post("/users", response_model=UserRead)
def create_user(user_in: UserCreate, session: SessionDep):
    hashed_pwd = hash_password(user_in.password)
    extra_user = User(
        email = user_in.email, 
        username = user_in.username, 
        password_hash= hashed_pwd
    )
    session.add(extra_user)
    session.commit()
    session.refresh(extra_user)
    return extra_user


