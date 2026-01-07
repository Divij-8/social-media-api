"""Posts router for creating, reading, updating, and deleting posts."""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import select, func
from app.models import Post, PostCreate, User, PostRead, PostUpdate, PostOut, Vote, Follow
from app.database import SessionDep
from app.oauth2 import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Posts"])

@router.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(
    post_in: PostCreate,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.id} creating post: {post_in.title[:50]}")
    new_post = Post(**post_in.model_dump(), user_id=current_user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

@router.get("/posts/{id}", response_model=PostOut) 
def get_post(id: int, session: SessionDep):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    votes = session.exec(select(func.count(Vote.post_id)).where(Vote.post_id == id)).one()
    return {"post": post, "votes": votes}

@router.get("/posts", response_model=list[PostOut])
def get_posts(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: str = "",
    mode: str = ""
):
    logger.info(f"User {current_user.id} fetching posts - mode: {mode}, search: {search}")
    stmt = (
        select(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .where(Post.title.like(f"%{search}%"))
        .where(Post.published == True)
    )
    if mode == "followed":
        subquery = (
            select(Follow.followed_id)
            .where(Follow.follower_id == current_user.id)
        )
        stmt = stmt.where(Post.user_id.in_(subquery))
    stmt = stmt.limit(limit).offset(offset)
    
    results = session.exec(stmt).all()
    return [{"post": post, "votes": votes} for post, votes in results]
    
@router.delete("/posts/{id}")
def delete_post(
    id: int,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.id} deleting post {id}")
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized"
        )
    
    session.delete(post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}")
def update_post(
    id: int,
    session: SessionDep,
    post_in: PostUpdate,
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.id} updating post {id}")
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    update_data = post_in.model_dump(exclude_unset=True)
    post.sqlmodel_update(update_data)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post



