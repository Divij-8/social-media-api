import logging
from app.models import User, UserCreate, UserRead
from app.database import SessionDep
from app.security import hash_password
from app.oauth2 import get_current_user
from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import select

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Users"])

@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, session: SessionDep):
    logger.info(f"Signup attempt for username: {user_in.username}")
    
    existing_user = session.exec(select(User).where((User.email == user_in.email) | (User.username == user_in.username))).first()
    if existing_user:
        logger.warning(f"Signup failed: email or username already exists")
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
    logger.info(f"User created successfully: {extra_user.username}")
    return extra_user

@router.get("/users/me", response_model=UserRead)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User profile requested: {current_user.username}")
    return current_user
