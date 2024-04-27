from users import UserModel
from datetime import datetime
from pydantic import BaseModel


class PostModel(BaseModel):
    id : int 
    content : str
    created_at : datetime
    updated_at : datetime
    user_id : int
    user = UserModel