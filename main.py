import getpass
import os
import sys

from database import database
from rooms import rooms_service
from users import users_service


def register_user(db):
    login = input("Login:")
    password = getpass.getpass("Password:")
    if not users_service.validate_login(login):
        print("Wrong login!")
        return
    if not users_service.validate_password(password):
        print("Wrong password!")
        return

    if users_service.has_user(db, login):
        print("User exists!")
        return

    users_service.create_user(db, login, password)

def login(db):
    login = input("Login:")
    password = getpass.getpass("Password:")

    return users_service.login(db, login, password)


def list_users(db, filter=None):
    for user in users_service.get_all_users(db):
        if filter is None:
            print(user.login)
        elif user.login.find(filter) > -1:
            print(user.login)


def remove_user(db, username):
    users_service.remove_user(db, username)


def create_room(db, user):
    rooms_service.create_room(db, user.login, getpass.getpass('Room password: '))


def delete_room(db, user):
    id = input("Room id: ")
    room = rooms_service.get_room(db, id)
    if room is None:
        print("Wrong room id!")
        return

    if room.owner != user.login:
        print("Wrong room id!")
        return

    rooms_service.delete_room_by_id(db, id)


def join_room(db, user):
    id = input("Room id:" )
    password = getpass.getpass("Room passowrd: ")

    if not rooms_service.join_room(db, user.login, id, password):
        print("Wrong room id or passowrd!")


def run():
    db = database.get_db(
        os.path.join(
            os.path.dirname(
                os.path.abspath(__name__)
            ), "db.csv")
    )

    if sys.argv[1] == "room":
        user = login(db)
        if user is None:
            print("Wrong credentials!")
            return

        if sys.argv[2] == "create":
            create_room(db, user)

        if sys.argv[2] == "delete":
            delete_room(db, user)

        if sys.argv[2] == "join":
            join_room(db, user)

    if sys.argv[1] == "user":
        if sys.argv[2] == "register":
            register_user(db)

        if sys.argv[2] == "login":
            user = login(db)
            if user is None:
                print("Wrong credentials!")
                return

            if sys.argv[3] == "list":
                list_users(db, None if len(sys.argv) < 5 else sys.argv[4])

        if sys.argv[2] == "remove":
            if len(sys.argv) < 4:
                print("Pass login to remove as last param")
                return
            user = login(db)
            if user is None:
                print("Wrong credentials!")

            remove_user(db, sys.argv[3])


if __name__ == '__main__':
    run()