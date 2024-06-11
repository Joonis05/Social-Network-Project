from typing import List
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import create_engine


engine = create_engine("postgresql://fabian:0205@localhost:5432/postgres")


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    This class represents a user in the database.

    Attributes:
        id (int): The user's ID.
        name (str): The user's name.
        username (str): The user's username.
        email (str): The user's email address.
        password (str): The user's password.
        biography (str): The user's biography.
        profile_picture (str): The user's profile picture.
        created_at (datetime): The user's creation date and time.
        updated_at (datetime): The user's last update date and time.
        followers (List[Followers]): A list of followers for the user.
        following (List[Following]): A list of following users for the user.
        posts (List[Post]): A list of posts made by the user.

    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    biography: Mapped[str] = mapped_column(String, nullable=True)
    profile_picture: Mapped[str] = mapped_column(String, nullable=True)
    created_at = mapped_column(DateTime(), default=datetime.utcnow, nullable=False)
    updated_at = mapped_column(
        DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    followers: Mapped[List["Followers"]] = relationship(back_populates="user")
    following: Mapped[List["Following"]] = relationship(back_populates="user")
    posts: Mapped[List["Post"]] = relationship(back_populates="user")


class Followers(Base):
    """
    This class represents a user's followers in the database.

    Attributes:
        user_id (int): The ID of the user.
        follower_id (int): The ID of the follower.
        user (User): The user object.
    """

    __tablename__ = "followers"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    follower_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    user: Mapped["User"] = relationship(back_populates="followers")


class Following(Base):
    """
    This class represents a user's following users in the database.

    Attributes:
        user_id (int): The ID of the user.
        following_id (int): The ID of the following user.
        user (User): The user object.
    """

    __tablename__ = "following"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    following_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    user: Mapped["User"] = relationship(back_populates="following")


class Post(Base):
    """
    This class represents a post in the database.

    Attributes:
        id (int): The post's ID.
        content (str): The post's content.
        created_at (datetime): The post's creation date and time.
        user_id (int): The ID of the user who made the post.
        user (User): The user object.
        comments (List[Comments]): A list of comments made on the post.
    """

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comments"]] = relationship(back_populates="post")


class Comments(Base):
    """
    This class represents a comment in the database.

    Attributes:
        id (int): The comment's ID.
        content (str): The comment's content.
        created_at (datetime): The comment's creation date and time.
        updated_at (datetime): The comment's last update date and time.
        user_id (int): The ID of the user who made the comment.
        post_id (int): The ID of the post the comment is on.
        post (Post): The post object.
    """

    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))

    post: Mapped["Post"] = relationship(back_populates="comments")


if __name__ == "__main__":

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
