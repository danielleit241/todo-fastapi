from fastapi import APIRouter, Depends, HTTPException, status
from .. import models
from ..database import get_db
from ..schemas import user as user_schemas
from ..utils.hashing import Hash
from ..config import settings
from ..utils.jwt import get_current_user

router = APIRouter(
    prefix=settings.API_PREFIX + "/users",
    tags=["Users"]
)

@router.get("", response_model=list[user_schemas.UserResponse])
def get_all_users(db=Depends(get_db), current_user=Depends(get_current_user)):
    users = db.query(models.User).all()
    return users

@router.get("/{id}", response_model=user_schemas.UserResponse)
def get_user_by_id(id: int, db=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserResponse)
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