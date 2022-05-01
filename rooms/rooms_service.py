import bcrypt

from database.database import Database
from database.rooms_model import Room


def create_room(db: Database, owner_login: str, password: str):
    rooms = db.find_all_in_db('ROOM')
    new_id = 0 if len(rooms) == 0 else str(int(rooms[-1][1]) + 1)
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    db.put_to_db('ROOM', new_id, owner_login, password)


def get_room(db: Database, id: str):
    db_room = db.find_in_db('ROOM', id)
    if db_room is None:
        return None

    return Room(id=db_room[1], owner=db_room[2], password=db_room[3])


def delete_room_by_id(db: Database, id: str):
    db.remove_from_db('ROOM', id)
    db.remove_from_db('JOIN', id)


def join_room(db: Database, user_login: str, id: str, password: str) -> bool:
    room = get_room(db, id)
    if room is None:
        return False

    if not bcrypt.checkpw(password.encode('utf-8'), room.password.encode('utf-8')):
        return False

    db.put_to_db('JOIN', id, user_login)
    return True
