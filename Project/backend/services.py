from fastapi import FastAPI
import uvicorn
from models import UserModel, UserCredentials, FollowModel, PostModel, CommentModel
import hashlib
from sqlalchemy.orm import sessionmaker
from database import engine
from database import User, Followers, Following, Post, Comments

Session = sessionmaker(bind=engine)
session = Session()



app = FastAPI()

@app.get("/")
def main():
    return "Hello World!"

@app.post("/create_user")
def create_user(nuser: UserModel):
    
    """
    This function creates a new user in the database

    Parameters:
    nuser (UserModel): A UserModel object containing the user's information

    Returns:
    dict: A dictionary containing a message indicating whether the user was created successfully or not

    """
    
    query = session.query(User).filter_by(username=nuser.username).first()
    email = session.query(User).filter_by(email=nuser.email).first()
    if query or email:
        return {"message": "User already exists"}
    else: 
        encode_password = nuser.password.encode("utf-8")
        user = User(
                    name=nuser.name, 
                    username=nuser.username, 
                    email=nuser.email,
                    password= hashlib.sha256(encode_password).hexdigest(),
                    biography=nuser.biography,
                    profile_picture=nuser.profile_picture,    
                )
    
        session.add(user)
        session.commit()
        return {"message": "User created successfully"}


@app.post("/authenticate_user")
def authenticate_user(userc: UserCredentials):
    """
    This function authenticates a user based on their username and password

    Parameters:
    userc (UserCredentials): A UserCredentials object containing the user's username and password

    Returns:
    dict: A dictionary containing a message indicating whether the user was authenticated successfully or not

    """
    query = session.query(User).filter_by(username=userc.username).first()
    if query:
        encode_password = userc.password.encode("utf-8")
        password_hash = hashlib.sha256(encode_password).hexdigest()
        user_password = query.password

        if password_hash == user_password:
            return {"message": "User authenticated successfully"}
        else:
            return {"message": "Invalid password"}
    else:
        return {"message": "Invalid username"}


@app.get("/get_user")
def get_user(user_id: int):
    """
    This function retrieves a user from the database based on their ID

    Parameters:
    user_id (int): The ID of the user to retrieve

    Returns:
    dict: A dictionary containing the user's information
    """
    query = session.query(User).filter_by(id=user_id).first()
    if query:
        return {"name": query.name, 
                "username": query.username, 
                "biography": query.biography, 
                "profile_picture": query.profile_picture}
    else:
        return {"message": "User not found"}


@app.put("/follow_user")
def follow_user(follow: FollowModel):
    """
    This function follows a user based on their username

    Parameters:
    follow (FollowModel): A FollowModel object containing the username of the user to follow

    Returns:
    dict: A dictionary containing a message indicating whether the user was followed successfully or not
    """

    query1 = session.query(User).filter_by(username=follow.follower).first()
    query2 = session.query(User).filter_by(username=follow.followed).first()

    if query1 and query2:
        id1 = Following(user_id=query2.id, following_id=query1.id)
        id2 = Followers(user_id=query1.id, follower_id=query2.id)

        query1.following.append(id1)
        query2.followers.append(id2)
        session.commit()
        return {"message": "User followed successfully"}
    else:
        return {"message": "Invalid username"}
    
@app.put("/unfollow_user")
def unfollow_user(unfollow: FollowModel):
    """
    This function unfollows a user based on their username

    Parameters:
    unfollow (FollowModel): A FollowModel object containing the username of the user to unfollow

    Returns:
    dict: A dictionary containing a message indicating whether the user was unfollowed successfully or not
    """
    #TODO add unfollow logic

    query1 = session.query(User).filter_by(username=unfollow.follower).first()
    query2 = session.query(User).filter_by(username=unfollow.followed).first()

    if query1 and query2:
        id1 = Following(user_id=query2.id, following_id=query1.id)
        id2 = Followers(user_id=query1.id, follower_id=query2.id)

        query1.following.remove(id1)
        query2.followers.remove(id2)
        session.commit()
        return {"message": "User unfollowed successfully"}
    else:
        return {"message": "Invalid username"}
    
@app.get("/get_followers")
def get_followers(username: str):
    """
    This function retrieves the followers of a user based on their username

    Parameters:
    username (str): The username of the user whose followers to retrieve

    Returns:
    dict: A dictionary containing a list of the user's followers
    """

    query = session.query(User).filter_by(username=username).first()
    if query:
        followers = []
        for i in query.followers:
            id_ = i.user_id
            user = get_user(id_)
            followers.append(user["username"])

        return {"followers": followers}
    else:
        return {"message": "User not found"}
    
@app.get("/get_following")
def get_following(username: str):
    """
    This function retrieves the following of a user based on their username

    Parameters:
    username (str): The username of the user whose following to retrieve

    Returns:
    dict: A dictionary containing a list of the user's following
    """

    query = session.query(User).filter_by(username=username).first()
    if query:
        following = []
        for i in query.following:
            id_ = i.user_id
            user = get_user(id_)
            following.append(user["username"])

        return {"following": following}
    else:
        return {"message": "User not found"}
    
app.post("/create_post")
def create_post(post: PostModel):
    """
    This function creates a new post in the database

    Parameters:
    post (PostModel): A PostModel object containing the post's information

    Returns:
    dict: A dictionary containing a message indicating whether the post was created successfully or not

    """
    query = session.query(User).filter_by(username=post.username).first()
    if query:
        post = Post(content=post.content, user_id=query.id)
        query.posts.append(post)
        session.commit()
        return {"message": "Post created successfully"}
    else:
        return {"message": "Invalid username"}

app.get("/get_posts")
def get_posts(username: str):
    """
    This function retrieves the posts of a user based on their username

    Parameters:
    username (str): The username of the user whose posts to retrieve

    Returns:
    dict: A dictionary containing a list of the user's posts
    """

    query = session.query(User).filter_by(username=username).first()
    if query:
        posts = []
        for i in query.posts:
            post = i.content
            posts.append(post)

        return {"posts": posts}
    else:
        return {"message": "User not found"}
    
@app.post("/create_comment")
def create_comment(comment: CommentModel):
    """
    This function creates a new comment in the database

    Parameters:
    comment (CommentModel): A CommentModel object containing the comment's information

    Returns:
    dict: A dictionary containing a message indicating whether the comment was created successfully or not

    """
    queryu = session.query(User).filter_by(username=comment.username).first()
    queryp = session.query(Post).filter_by(id=comment.post_id).first()
    if queryu and queryp:
        comment = Comments(content=comment.content, user_id=queryu.id, post_id=comment.post_id)
        queryp.comments.append(comment)
        session.commit()
        return {"message": "Comment created successfully"}
    else:
        return {"message": "Invalid username"}



    

if __name__ == "__main__":

    user1 = UserModel(name="John", username="john", email="john@example.com", password="password", biography="I am a student", profile_picture="https://example.com/john.jpg")
    user2 = UserModel(name="Jane", username="jane", email="jane@example.com", password="password", biography="I am a teacher", profile_picture="https://example.com/jane.jpg")
    user3 = UserModel(name="Bob", username="bob", email="bob@example.com", password="password", biography="I am a teacher", profile_picture="https://example.com/bob.jpg")
    user4 = UserModel(name="Alice", username="alice", email="alice@example.com", password="password", biography="I am a student", profile_picture="https://example.com/alice.jpg")
    user5 = UserModel(name="Bob", username="bob", email="bob1@example.com", password="password", biography="I am a teacher", profile_picture="https://example.com/bob.jpg")

    print(create_user(user1))
    print(create_user(user2))
    print(create_user(user3))
    print(create_user(user4))
    print(create_user(user5))

    post1 = PostModel(content="This is a post", username="john")
    post2 = PostModel(content="This is another post", username="jane")
    post3 = PostModel(content="This is a post", username="bob")

    print(create_post(post1))
    print(create_post(post2))
    print(create_post(post3))

    comment1 = CommentModel(content="This is a comment", username="john", post_id=1)
    comment2 = CommentModel(content="This is another comment", username="jane", post_id=1)
    comment3 = CommentModel(content="This is a comment", username="bob", post_id=1)

    print(create_comment(comment1))
    print(create_comment(comment2))
    print(create_comment(comment3))

    




    


    #uvicorn.run("services:app", host="localhost", port=8000)