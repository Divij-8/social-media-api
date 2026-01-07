from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship # type: ignore
from typing import List, Optional, Annotated
from pydantic import EmailStr # type: ignore
    

Email = Annotated[EmailStr, Field(index=True, unique=True, max_length=128)]
Username = Annotated[str, Field(index=True, unique=True, min_length=3, max_length=128)]

class UserBase(SQLModel):
    email: Email # type: ignore
    username: Username # type: ignore


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class User(UserBase, table=True):
    __tablename__ = "users_v2"
    id: Optional[int] = Field(primary_key=True, default=None)  
    password_hash: str 
    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    posts: List["Post"] = Relationship(back_populates="user")
    


class UserRead(UserBase):
    id: int
    created_at: datetime
    

class UserUpdate(UserBase):
    email: Optional[Email] = None # type: ignore
    username: Optional[Username] = None # type: ignore


class PostBase(SQLModel):
    title: str
    content: str
    


class Post(PostBase, table=True):
    __tablename__ = "posts"
    id: Optional[int] = Field(primary_key=True, default=None) 
    user_id: int = Field(foreign_key="users_v2.id")    
    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    user: Optional["User"] = Relationship(back_populates="posts")
    published: bool = Field(default=True)


class PostCreate(PostBase):
    pass


class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostRead(PostBase):
    id: int
    created_at: datetime
    user_id: int
    published: bool
    

class Vote(SQLModel, table=True):
    __tablename__ = "votes"

    user_id: int = Field(foreign_key="users_v2.id", primary_key=True)
    post_id: int =Field(foreign_key="posts.id", primary_key=True)

class VoteCreate(SQLModel):
    post_id: int
    dir: int = Field(le=1)


class PostOut(SQLModel):
    post: PostRead
    votes: int


class Follow(SQLModel, table=True):
    __tablename__ = "follows"

    follower_id: int = Field(foreign_key="users_v2.id", primary_key=True)
    followed_id: int = Field(foreign_key="users_v2.id", primary_key=True)


class FollowCreate(SQLModel):
    followed_id: int





