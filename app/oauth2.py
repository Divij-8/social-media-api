from datetime import datetime, timedelta, timezone
import jwt
from sqlmodel import Session, select
from config import settings
from models import User
from security import verify_password


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str, session: Session):
    query = select(User).where(User.username == username)
    user = session.exec(query).first()

    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user

