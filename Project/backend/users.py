from pydantic import BaseModel, EmailStr
from datetime import datetime, date


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

