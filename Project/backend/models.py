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

class FollowModel(BaseModel):
    follower: str
    followed: str

class PostModel(BaseModel):
    id : int = None
    content : str
    username : str

class CommentModel(BaseModel):
    id : int = None
    content : str
    username : str
    post_id : int 