from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine("postgresql://joonis:0205@localhost/db_joonis")
Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id : Mapped[int]  = mapped_column(Integer(), primary_key=True)
    name : Mapped[str] = mapped_column(String(50), nullable=False)
    username : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    birthday : Mapped[str] = mapped_column(DateTime.date)
    email : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password : Mapped[str] = mapped_column(String(50), nullable=False)
    biography: Mapped[str] = mapped_column(String, nullable=True)
    profile_picture : Mapped[str] = mapped_column(String, nullable=True)
    created_at = mapped_column(DateTime(), default=datetime.utcnow, nullable=False)
    updated_at = mapped_column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __str__(self):
        return self.username


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



