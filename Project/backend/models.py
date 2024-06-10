from pydantic import BaseModel

class UserModel(BaseModel):
    name: str
    username: str
    email: str
    password: str
    biography: str = None
    profile_picture: str = None
    
class UserCredentials(BaseModel):
    username: str
    password: str