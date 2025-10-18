from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app import models
from ..utils import jwt
from app.database import get_db
from app.schemas.vote import VoteCreate, VoteOfUserResponse, VoteOfPostResponse
from typing import List

router = APIRouter(
    prefix="/votes",
    tags=["Vote"]
)

@router.get("/users/{user_id}", response_model=List[VoteOfUserResponse])
def get_user_votes(user_id: int, db: Session = Depends(get_db)):
    vote = db.query(models.Vote).options(joinedload(models.Vote.post)).filter(models.Vote.user_id == user_id).all()
    if not vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No votes found for user with id {user_id}.")
    return vote

@router.get("/posts/{post_id}", response_model=List[VoteOfPostResponse])
def get_votes(post_id: int, db: Session = Depends(get_db)):
    vote = db.query(models.Vote).options(joinedload(models.Vote.user)).filter(models.Vote.post_id == post_id).all()
    if not vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No votes found for post with id {post_id}.")
    return vote

@router.post("", status_code=status.HTTP_201_CREATED)
def vote(vote: VoteCreate, db: Session = Depends(get_db), current_user: int = Depends(jwt.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    voted = vote_query.first()
    if voted:
        db.delete(voted)
        db.commit()
        return {"message": "Successfully removed vote."}

    new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
    return {"message": "Successfully added vote."}
    