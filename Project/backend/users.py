from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import User 
import hashlib

engine = create_engine("")
Session = Session(engine)



class UserModel(BaseModel):

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
    username : str
    password : str

def create_user(user : UserModel):
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
        


