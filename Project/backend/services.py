from fastapi import FastAPI
import uvicorn
from database import User
from models import UserModel, UserCredentials
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import engine
from database import User

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




if __name__ == "__main__":

    #uvicorn.run("services:app", host="localhost", port=8000)