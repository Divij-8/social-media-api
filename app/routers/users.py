from app.models import User, UserCreate, UserRead
from app.database import SessionDep
from app.security import hash_password
from fastapi import APIRouter, status, HTTPException
from sqlmodel import select


router = APIRouter(tags=["Users"])


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, session: SessionDep):
    # Check if user with email or username already exists
    existing_user = session.exec(select(User).where((User.email == user_in.email) | (User.username == user_in.username))).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email or username already exists")
    
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
