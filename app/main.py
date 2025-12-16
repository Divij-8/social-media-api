from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from database import create_db_and_tables, SessionDep, get_session
from models import User, UserCreate, UserRead
from security import hash_password
from routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: Creating tables...")
    create_db_and_tables()
    yield
    print("Shutdown: Cleaning up...")


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)


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


