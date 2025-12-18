from models import User, UserCreate, UserRead
from database import SessionDep
from security import hash_password
from fastapi import APIRouter


router = APIRouter(tags=["Users"])


@router.post("/users")
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
