from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    published = Column(Boolean, default=True)
    vote = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default='now()')
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default='now()', onupdate='now()')
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="posts")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default='now()')
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default='now()', onupdate='now()')
    posts = relationship("Post", back_populates="owner")


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default='now()')
    user = relationship("User", backref="votes")
    post = relationship("Post", backref="votes")

