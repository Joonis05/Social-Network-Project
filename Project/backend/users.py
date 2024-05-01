import hashlib
from datetime import date, datetime

from database import User
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("")
Session = Session(engine)



class UserModel(BaseModel):
    """
    Represents a user model within the system.

    Attributes:
        id (int): Unique identifier for the user.
        name (str): Full name of the user.
        username (str): Unique username for login purposes.
        email (EmailStr): User's email address.
        password (str): User's password (stored encrypted).
        biography (str): Brief description about the user.
        birthday (date): User's date of birth.
        profile_picture (str): URL of the user's profile picture.
        created_at (datetime): Date and time the user was created.
    """

    id : int
    name : str
    username : str
    email : EmailStr
    password : str
    biography : str
    birthday: date
    profile_picture: str
    created_at : datetime.utcnow

class UserLogin(BaseModel):
    """
    Represents user credentials for login purposes.

    Attributes:
        username (str): User's unique username for login.
        password (str): User's password (assumed to be provided encrypted).
    """
    username : str
    password : str

def create_user(user : UserModel):
    """
    Creates a new user in the system.

    Args:
        user (UserModel): A UserModel object representing the new user.

    Raises:
        ValueError:
            - If the user's name is less than 3 characters or greater than 64 characters.
            - If the user's username is less than 3 characters or greater than 64 characters.
            - If the user's password is empty.
            - If the user's birthday is in the future.

    Returns:
        UserModel: The newly created user object.
    """
    if len(user.name) < 3 or len(user.username) > 64:
        raise ValueError("The name must be between 3 and 64 characters")
    if len(user.username) < 3 or len(user.username) > 64:
        raise ValueError("The username must be between 3 and 64 characters")
    if not user.password:
        raise ValueError("The password is required")
    if user.birthday > datetime.utcnow():
        raise ValueError("The birthday must be in the past")

    password_hash = hashlib.sha256(user.password)
    new_user = User(
        name = user.name,
        username = user.username,
        email = user.email,
        password = password_hash,
        biography = user.biography,
        birthday = user.birthday,
        profile_picture = user.profile_picture
        )

    Session.add(new_user)
    Session.commit()
    return new_user
        


