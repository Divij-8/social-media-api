"""Authentication router for user login."""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.database import SessionDep
from app.oauth2 import authenticate_user, create_access_token

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    logger.info(f"Login attempt for username: {user_credentials.username}")
    user = authenticate_user(user_credentials.username, user_credentials.password, session)
    if not user:
        logger.warning(f"Login failed for username: {user_credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    access_token = create_access_token(data={"user_id": user.id})
    logger.info(f"User {user.username} logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}