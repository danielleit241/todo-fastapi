from fastapi import Depends, FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from app.seed import seed_data
from . import models
from .database import get_db

seed_data()

app = FastAPI()

class Post(BaseModel): 
    id: int
    title: str
    content: str
    published: bool = True
    vote: Optional[int] = None

@app.get("/posts", response_model=list[Post])
def read_posts(db=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=Post)
def get_post_by_id(id: int, db=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
