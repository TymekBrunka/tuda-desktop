import sqlite3
from typing import Annotated
from fastapi import FastAPI, HTTPException, Cookie, exceptions
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from hashlib import sha256

from os import mkdir, path

from shared import *

class ProjectCreation(BaseModel):
    name: str

@app.post("/projects/create")
async def create_project(cookies: Annotated[Cookies, Cookie()], data: ProjectCreation):
    user = getUser(cookies.email, cookies.hash)
    if not user:
        raise HTTPException(status_code=400, detail="Niezalogowano lub błędne dane logowania")

    if not path.exists(f"/data/projects/{user[0]}/"):
        try:
            mkdir(f"/data/projects/{user[0]}/")
        except:
            raise HTTPException(status_code=500, detail="Nie można było utworzyc nowego projektu")

    try:
        DBconn = sqlite3.connect(f"/data/projects/{user[0]}/{data.name}")
    except:
        raise HTTPException(status_code=500, detail="Nie można było utworzyc nowego projektu")
    DB = usersDBconn.cursor()

    DB.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email TEXT NOT NULL,
    );

    CREATE TABLE IF NOT EXISTS task (
        id INTEGER PRIMARY KEY,
        content TEXT,
        deadline REAL,
        status INT2
    );
    ''')
    DBconn.commit()
