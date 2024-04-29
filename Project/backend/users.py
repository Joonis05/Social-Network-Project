from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models import User 
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
    created_at : datetime

    @classmethod
    def create_user(name, username, email, password, birthday, profile_picture=None, biography=None, ):

        password_hash = hashlib.sha256(password)
        new_user = User(
            name = name,
            username = username,
            email = email,
            password = password_hash,
            biography = biography,
            birthday = birthday,
            profile_picture = profile_picture
        )

        Session.add(new_user)
        Session.commit()
        Session.close()
        


