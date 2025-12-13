from database import SessionDep
from sqlmodel import select, Session


def authenticate_user(username: str, password: str, session: SessionDep):
    user 