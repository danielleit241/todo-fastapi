from fastapi import Depends, FastAPI, HTTPException, status
from .seed import seed_data
from . import models
from .database import get_db
from .schemas import blog as blog_schemas, user as user_schemas
from .hashing import Hash

seed_data()

app = FastAPI()

@app.get("/posts", response_model=list[blog_schemas.PostResponse])
def get_all_posts(db=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=blog_schemas.PostResponse)
def get_post_by_id(id: int, db=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=blog_schemas.PostResponse)
def create_post(post: blog_schemas.PostCreate, db=Depends(get_db)):
    db_post = models.Post(
        title=post.title,
        content=post.content,
        published=post.published
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, updated_post: blog_schemas.PostCreate, db=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.title = updated_post.title
    post.content = updated_post.content
    post.published = updated_post.published

    db.commit()
    db.refresh(post)
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}

""" Header for User Endpoints """

@app.get("/users", response_model=list[user_schemas.UserResponse])
def get_all_users(db=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserResponse)
def create_user(user: user_schemas.UserCreate, db=Depends(get_db)):
    user_exist = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already registered")
    hash_password = Hash.argon2(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hash_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Auth 

@app.post("/login")
def login(user_credentials: user_schemas.UserLogin, db=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    if not Hash.verify_argon2(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    return {"detail": "Login successful"}


