from fastapi import FastAPI
import uvicorn
from models import UserModel, UserCredentials, FollowModel
import hashlib
from sqlalchemy.orm import sessionmaker
from database import engine
from database import User, Followers, Following

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
    if query:
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
def get_user(username: str):
    query = session.query(User).filter_by(username=username).first()
    if query:
        return {"name": query.name, 
                "username": query.username, 
                "biography": query.biography, 
                "profile_picture": query.profile_picture}
    else:
        return {"message": "User not found"}


@app.put("/follow_user")
def follow_user(follow: FollowModel):
    query1 = session.query(User).filter_by(username=follow.followed).first()
    query2 = session.query(User).filter_by(username=follow.follower).first()
    if query1 and query2:
        id1 = Following(following_id=query1.id)
        id2 = Followers(following_id=query2.id)

        query1.following.append(id1)
        query2.following.append(id2)
        session.commit()
        return {"message": "User followed successfully"}
    else:
        return {"message": "Invalid username"}
    
@app.get("/get_followers")
def get_followers(username: str):
    query = session.query(User).filter_by(username=username).first()
    if query:
        return {"followers": query.followers}
    else:
        return {"message": "User not found"}
    
@app.get("/get_following")
def get_following(username: str):
    query = session.query(User).filter_by(username=username).first()
    if query:
        return {"following": query.following}
    else:
        return {"message": "User not found"}

if __name__ == "__main__":

    #uvicorn.run("services:app", host="localhost", port=8000)