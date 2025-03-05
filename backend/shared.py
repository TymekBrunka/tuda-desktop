from sqlite3 import Connection, Cursor
from fastapi import FastAPI,
from pydantic import BaseModel

app: FastAPI
usersDBconn: sqlite3.Connection
usersDB: sqlite3.Cursor

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
