from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.user import UserResponse

class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner: Optional[UserResponse]
    total_votes: Optional[int] = 0
    model_config = {
        "from_attributes": True
    }

class PostResponseWithPagination(BaseModel):
    posts: List[PostResponse]
    total: int
    index: int
    limit: int
    model_config = {
        "from_attributes": True
    }