from pydantic import BaseModel


class UserModel(BaseModel):
    """
    This class represents a pydantic model for a user.

    Attributes:
        name (str): The user's name.
        username (str): The user's username.
        email (str): The user's email address.
        password (str): The user's password.
        biography (str): The user's biography.
        profile_picture (str): The user's profile picture.
    """

    name: str
    username: str
    email: str
    password: str
    biography: str = None
    profile_picture: str = None


class UserCredentials(BaseModel):
    """
    This class represents a pydantic model for user credentials.

    Attributes:
        username (str): The user's username.
        password (str): The user's password.
    """

    username: str
    password: str


class FollowModel(BaseModel):
    """
    This class represents a pydantic model for a follow relationship.

    Attributes:
        follower (str): The user who is following the user.
        followed (str): The user who is being followed.
    """

    follower: str
    followed: str


class PostModel(BaseModel):
    """
    This class represents a pydantic model for a post.

    Attributes:
        content (str): The content of the post.
        username (str): The username of the user who made the post.
    """

    id: int = None
    content: str
    username: str


class CommentModel(BaseModel):
    """
    This class represents a pydantic model for a comment.

    Attributes:
        content (str): The content of the comment.
        username (str): The username of the user who made the comment.
    """

    id: int = None
    content: str
    username: str
    post_id: int
