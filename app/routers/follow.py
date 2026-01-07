"""Follow router for managing user follows."""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from app.database import SessionDep
from app.models import Follow, User, FollowCreate
from app.oauth2 import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Follow"])

@router.post("/follow", status_code=status.HTTP_201_CREATED)
def follow_user(
    follow_in: FollowCreate,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.id} attempting to follow user {follow_in.followed_id}")
    
    if follow_in.followed_id == current_user.id:
        logger.warning(f"User {current_user.id} attempted to follow themselves")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users cannot follow themselves"
        )
    
    followed_user = session.get(User, follow_in.followed_id)
    if not followed_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User to follow not found"
        )
    
    query = select(Follow).where(
        Follow.follower_id == current_user.id,
        Follow.followed_id == follow_in.followed_id
    )
    found_follow = session.exec(query).first()
    
    if found_follow:
        logger.warning(f"User {current_user.id} already following user {follow_in.followed_id}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already following this user"
        )
    
    new_follow = Follow(
        follower_id=current_user.id,
        followed_id=follow_in.followed_id
    )
    session.add(new_follow)
    session.commit()
    logger.info(f"User {current_user.id} successfully followed user {follow_in.followed_id}")
    
    return {"message": "Successfully followed the user"}

@router.delete("/unfollow/{followed_id}", status_code=status.HTTP_200_OK)
def unfollow_user(
    followed_id: int,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.id} attempting to unfollow user {followed_id}")
    
    if followed_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot unfollow yourself"
        )
    
    query = select(Follow).where(
        Follow.follower_id == current_user.id,
        Follow.followed_id == followed_id
    )
    found_follow = session.exec(query).first()
    
    if not found_follow:
        logger.warning(f"User {current_user.id} not following user {followed_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not following this user"
        )
    
    session.delete(found_follow)
    session.commit()
    logger.info(f"User {current_user.id} successfully unfollowed user {followed_id}")
    
    return {"message": "Successfully unfollowed the user"}


