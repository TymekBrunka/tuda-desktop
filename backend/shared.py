from sqlite3 import Connection, Cursor, connect
from fastapi import FastAPI
from pydantic import BaseModel

app: FastAPI = FastAPI()
usersDBconn: Connection
usersDB: Cursor

try:
    usersDBconn = connect("data/users.db")
except Exception as ex:
    print(ex)
    exit()
usersDB = usersDBconn.cursor()

class Cookies(BaseModel):
    email: str
    hash: str

def getUser(email: str, hash: str):

    usersDB.execute('''
    SELECT * from Users WHERE email = ? AND password = ? LIMIT 1;
    ''', (
        email,
        hash
    ))
    user = usersDB.fetchone()
    return user
