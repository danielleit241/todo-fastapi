from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    published = Column(Boolean, default=True)
    vote = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default='now()')
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default='now()', onupdate='now()')