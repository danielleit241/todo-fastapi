from fastapi import APIRouter, Depends, HTTPException, status

from app.utils.jwt import get_current_user
from .. import models
from ..database import get_db
from ..schemas import post as post_schemas

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("", response_model=list[post_schemas.PostResponse])
def get_all_posts(db=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get("/{id}", response_model=post_schemas.PostResponse)
def get_post_by_id(id: int, db=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("", status_code=status.HTTP_201_CREATED, response_model=post_schemas.PostResponse)
def create_post(post: post_schemas.PostCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    db_post = models.Post(
        title=post.title,
        content=post.content,
        published=post.published,
        owner_id=current_user.id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, updated_post: post_schemas.PostCreate, db=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.title = updated_post.title
    post.content = updated_post.content
    post.published = updated_post.published

    db.commit()
    db.refresh(post)
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}