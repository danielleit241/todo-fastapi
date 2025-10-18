from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse
from app.schemas.post import PostResponse
from typing import List

class VoteBase(BaseModel):
    post_id: int
    user_id: int

class VoteCreate(VoteBase):
    pass

class VoteOfPostResponse(BaseModel):
    created_at: datetime
    user: Optional[UserResponse]
    model_config = {
        "from_attributes": True
    }

class VoteOfUserResponse(BaseModel):
    created_at: datetime
    post: Optional[PostResponse]
    model_config = {
        "from_attributes": True
    }