from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from ..utils.jwt import get_current_user
from .. import models
from ..database import get_db
from ..schemas import post as post_schemas
from ..config import settings

router = APIRouter(
    prefix=settings.API_PREFIX + "/posts",
    tags=["Posts"]
)

@router.get("", response_model=post_schemas.PostResponseWithPagination)
def get_all_posts(db=Depends(get_db), limit: int = 10, skip: int = 0, keyword: Optional[str] = None):
    query = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("total_votes")
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(models.Post.id)

    if keyword:
        query = query.filter(models.Post.title.contains(keyword))

    total_posts = query.count()
    posts = query.offset(skip).limit(limit).all()

    result_posts = []
    for post, total_votes in posts:
        post_data = post_schemas.PostResponse.model_validate(post)
        post_data.total_votes = total_votes
        result_posts.append(post_data)

    return post_schemas.PostResponseWithPagination(
        posts=result_posts,
        total=total_posts,
        index=skip,
        limit=limit
    )

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
def update_post(id: int, updated_post: post_schemas.PostCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    post.title = updated_post.title
    post.content = updated_post.content
    post.published = updated_post.published

    db.commit()
    db.refresh(post)
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}