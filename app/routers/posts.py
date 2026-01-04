from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import select, func
from app.models import Post, PostCreate, User, PostRead, PostUpdate, PostOut, Vote, Follow
from app.database import SessionDep
from app.oauth2 import get_current_user



router = APIRouter(tags=["Posts"])


@router.post("/posts", response_model=PostRead)
def create_post(
    post_in: PostCreate,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    new_post = Post(**post_in.model_dump(), user_id=current_user.id)

    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return new_post


@router.get("/posts", response_model=list[PostOut])
def get_posts(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: str = "",
    mode: str = ""
):
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



