from fastapi import FastAPI
import uvicorn
from models import UserModel, UserCredentials, FollowModel, PostModel
import hashlib
from sqlalchemy.orm import sessionmaker
from database import engine
from database import User, Followers, Following, Post

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
    query1 = session.query(User).filter_by(username=unfollow.followed).first()
    query2 = session.query(User).filter_by(username=unfollow.follower).first()

    if query1 and query2:
        id1 = Following(user_id=query2.id, following_id=query1.id)
        id2 = Followers(user_id=query1.id, follower_id=query2.id)

        query1.following.remove(id2)
        query2.followers.remove(id1)
        session.commit()
        return {"message": "User followed successfully"}
    else:
        return {"message": "Invalid username"}
    
@app.get("/get_followers")
def get_followers(username: str):
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
    query = session.query(User).filter_by(username=username).first()
    if query:
        return {"following": query.following}
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

    """follow1 = FollowModel(follower="john", followed="bob")
    follow2 = FollowModel(follower="bob", followed="john")
    follow3 = FollowModel(follower="john", followed="alice")

    print(follow_user(follow1))
    print(follow_user(follow2))
    print(follow_user(follow3))"""


    print(get_followers("john"))
    


    


    #uvicorn.run("services:app", host="localhost", port=8000)