from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, Annotated
from pydantic import EmailStr
    

Email = Annotated[EmailStr, Field(index=True, unique=True, max_length=128)]
Username = Annotated[str, Field(index=True, unique=True, min_length=3, max_length=128)]

class UserBase(SQLModel):
    email: Email # type: ignore
    username: Username # type: ignore


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(primary_key=True, default=None)  
    password_hash: str 
    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    posts: List["Post"] = Relationship(back_populates="user")
    


class UserRead(UserBase):
    id: int
    created_at: datetime
    

class UserUpdate(UserBase):
    email: Email | None = None # type: ignore
    username: Username | None = None # type: ignore


class PostBase(SQLModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase, table=True):
    __tablename__ = "posts"
    id: Optional[int] = Field(primary_key=True, default=None) 
    user_id: int = Field(foreign_key="users.id")    
    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    user: Optional["User"] = Relationship(back_populates="posts")


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserRead
    










