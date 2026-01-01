from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from app.database import SessionDep
from app.models import Follow, User, FollowCreate
from app.oauth2 import get_current_user


router = APIRouter(tags=["Follow"])

@router.post("/follow", status_code=status.HTTP_201_CREATED)
def follow_user(
    follow_in: FollowCreate,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    if follow_in.followed_id == current_user.id:
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
    
    return {"message": "Successfully followed the user"}


@router.delete("/unfollow", status_code=status.HTTP_200_OK)
def unfollow_user(
    follow_in: FollowCreate,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    query = select(Follow).where(
        Follow.follower_id == current_user.id,
        Follow.followed_id == follow_in.followed_id
    )
    found_follow = session.exec(query).first()
    
    if not found_follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not following this user"
        )
    
    session.delete(found_follow)
    session.commit()
    
    return {"message": "Successfully unfollowed the user"}


