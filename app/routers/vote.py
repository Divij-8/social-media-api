from fastapi import APIRouter, Depends, HTTPException, status
from app.database import SessionDep
from app.models import Vote, VoteCreate, Post, User
from app.oauth2 import get_current_user
from sqlmodel import select

router = APIRouter(tags=["Vote"])

@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(
    vote: VoteCreate,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    
    post = session.get(Post, vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    query = select(Vote).where(
        Vote.post_id == vote.post_id,
        Vote.user_id == current_user.id
    )
    found_vote = session.exec(query).first()    

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has already voted on this post"
            )
        
        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message": "Vote added successfully"}
    
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist"
            )
        
        session.delete(found_vote)
        session.commit()
        return {"message": "Vote removed successfully"}
