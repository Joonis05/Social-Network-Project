from faker import Faker
from models import UserModel, FollowModel, PostModel, CommentModel
from database import engine, Base
from sqlalchemy.orm import sessionmaker
from services import create_user, follow_user, create_post, create_comment

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()
DATA = 10


def generate_user_data():
    """
    This function generates a user data

    Returns:
        UserModel: A user model
    """
    name = fake.name()
    username = fake.unique.user_name()
    email = fake.unique.email()
    password = fake.password()
    biography = fake.text(10)
    return UserModel(
        name=name,
        username=username,
        email=email,
        password=password,
        biography=biography,
    )


def generate_follow_data(usernames: list):
    """
    This function generates a follow data

    Args:
        usernames (list): A list of usernames

    Returns:
        FollowModel: A follow model
    """
    follower = fake.random.choice(usernames)
    followed = fake.random.choice(usernames)
    return FollowModel(follower=follower, followed=followed)


def generate_post_data(usernames: list):
    """
    This function generates a post data

    Args:
        usernames (list): A list of usernames

    Returns:
        PostModel: A post model
    """
    content = fake.image_url()
    username = fake.random.choice(usernames)
    return PostModel(content=content, username=username)


def generate_comment_data(usernames: list):
    """
    This function generates a comment data

    Args:
        usernames (list): A list of usernames

    Returns:
        CommentModel: A comment model
    """
    content = fake.text(10)
    username = fake.random.choice(usernames)
    post_id = fake.random.randint(1, DATA)
    return CommentModel(content=content, username=username, post_id=post_id)


if __name__ == "__main__":

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    users = []
    usernames = []
    for i in range(DATA):
        users.append(generate_user_data())
        create_user(users[i])

    for i in users:
        usernames.append(i.username)

    for i in range(DATA):
        follow = generate_follow_data(usernames)
        follow_user(follow)

    for i in range(DATA):
        post = generate_post_data(usernames)
        create_post(post)

    for i in range(DATA):
        comment = generate_comment_data(usernames)
        create_comment(comment)
