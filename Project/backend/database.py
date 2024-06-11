from typing import List
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import create_engine


engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id : Mapped[int]  = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(64), nullable=False)
    username : Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    email : Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password : Mapped[str] = mapped_column(String, nullable=False)
    biography: Mapped[str] = mapped_column(String, nullable=True)
    profile_picture : Mapped[str] = mapped_column(String, nullable=True)
    created_at = mapped_column(DateTime(), default=datetime.utcnow, nullable=False)
    updated_at = mapped_column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    followers : Mapped[List["Followers"]] = relationship(back_populates="user")
    following : Mapped[List["Following"]] = relationship(back_populates="user")

class Followers(Base):
    __tablename__ = "followers"
    followers_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    user : Mapped["User"] = relationship(back_populates="followers")

class Following(Base):
    __tablename__ = "following"
    following_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    user : Mapped["User"] = relationship(back_populates="following")

class Post(Base):
    __tablename__ = "posts"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    content : Mapped[str] = mapped_column(String, nullable=False)
    created_at : Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at : Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    user = Relationship("User", back_populates="posts")

class Comments(Base):
    __tablename__ = "comments"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    content : Mapped[str] = mapped_column(String, nullable=False)
    created_at : Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at : Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    post_id : Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))
    
    
    user = Relationship("User", back_populates="comments")
    post = Relationship("Post", back_populates="comments")

if __name__ == "__main__":

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



