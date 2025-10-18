from datetime import datetime
from pydantic import BaseModel, EmailStr
from . import post as post_schemas

class UserBase(BaseModel):
    email: EmailStr 

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    posts: list[post_schemas.PostResponse] = []
    class Config:
        orm_mode = True

class UserLogin(UserBase):
    password: str


