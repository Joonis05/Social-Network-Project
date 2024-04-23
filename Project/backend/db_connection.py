from sqlalchemy import String, Integer, DateTime, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine("postgresql://joonis:0205@localhost/db_joonis")
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id : Mapped[int]  = mapped_column(Integer(), primary_key=True)
    username : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at = mapped_column(DateTime(), default=datetime.now)

    def __str__(self):
        return self.username
    
Session = sessionmaker(engine)
session = Session()

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    user1 = User(username= "user1", email="user1example@gmail.com, ")
    user2 = User(username= "user2", email="user2example@gmail.com, ")
    user3 = User(username= "user3", email="user3example@gmail.com, ")

    session.add(user1)
    session.add(user2)
    session.add(user3)
    
    session.commit()



