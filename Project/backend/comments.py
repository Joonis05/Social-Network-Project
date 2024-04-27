from users import UserModel
from posts import PostModel
from datetime import datetime
from pydantic import BaseModel

class CommentModel(BaseModel):
    d: int
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    post_id: int
    user: UserModel
    post: PostModel

