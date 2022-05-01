import os
import sqlite3
from sys import argv
from os import getenv
from sqlite3 import Error


class Database:

    def __init__(self, **kwargs):
        self.connection = None
        self.cursor = None
        self.db = os.path.join(self.path, '/identifier.sqlite')
        self.path = os.path.dirname(os.path.abspath('.'))

    def get_database(self):
        self.connection = sqlite3.connect(self.db)
        print("init")
        print(sqlite3.version)
        self.cursor = self.connection.cursor()

    def createTableUsers(self):
        self.cursor.execute('''
        CREATE TABLE users (
        user_id integer PRIMARY KEY,
        login text NOT NULL UNIQUE,
        password text NOT NULL
        )
        ''')

    def createTableRooms(self):
        self.cursor.execute('''
        CREATE TABLE rooms (
        room_id integer PRIMARY KEY,
        password text NOT NULL,
        owner_id integer NOT NULL,
        FOREIGN KEY (room_id)
        REFERENCES users (user_id) 
        )
        ''')

    def selectFromUsers(self):
        self.connection.execute("SELECT * FROM users")
        all_users = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM users WHERE login = \"A\"")
        one_user = self.cursor.fetchone()

    def insertIntoRooms(self, one_user=None):
        self.cursor.execute(
            "INSERT INTO rooms (password, owner_id) VALUES (\"password\", {}) RETURNING *".format(one_user[0]))
        created_room = self.cursor.fetchone()

    def remove_from_db(self, param, param1):
        pass

    def find_all_in_db(self, param):
        pass

    def commitToDatabase(self):
        self.connection.commit()
        self.cursor.execute("INSERT INTO users (login, password) VALUES(\"A\", \"B\")")
        self.connection.commit()

    def closeConnection(self):
        self.connection.close()
