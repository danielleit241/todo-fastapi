from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    vote: int | None = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class PostResponseWithPagination(BaseModel):
    posts: list[PostResponse]
    total: int
    index: int
    limit: int
    class Config:
        from_attributes = True