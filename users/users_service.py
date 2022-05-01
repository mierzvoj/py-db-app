import re
from typing import List

import bcrypt

from database.database import Database
from database.users_model import User

LOGIN_RE = r'^[a-zA-Z0-9]+$'


def validate_login(login: str):
    if not len(login) > 3:
        return False

    return re.match(LOGIN_RE, login) is not None


def validate_password(password):
    return len(password) > 4


def has_user(db: Database, login: str):
    return db.find_in_db('USER', login.lower()) is not None


def login(db: Database, login: str, password: str):
    user = db.find_in_db('USER', login.lower())
    if user is None:
        return None

    if not bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return None

    return User(login=user[1])


def create_user(db: Database, login: str, password):
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    db.put_to_db('USER', login.lower(), password)


def get_all_users(db: Database) -> List[User]:
    return [User(login=row[1]) for row in db.find_all_in_db('USER')]


def remove_user(db: Database, login):
    db.remove_from_db('USER', login.lower())
