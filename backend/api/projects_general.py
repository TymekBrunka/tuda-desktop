import sqlite3
from sys import exception
from typing import Annotated
from fastapi import FastAPI, HTTPException, Cookie, exceptions
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from hashlib import sha256
from uuid import uuid4

from os import makedirs, path, unlink

from shared import *

class ProjectCreation(BaseModel):
    name: str

@app.post("/projects/create")
async def create_project(cookies: Annotated[Cookies, Cookie()], item: ProjectCreation):
    """ kopiowanie danych do sanityzacji przed wstrzykiwaniem sql'a """
    name: str = item.name[:]
    name.replace('"', '\\"').replace("\\", "\\\\")

    user = getUser(cookies.email, cookies.hash)
    if not user:
        raise HTTPException(status_code=400, detail="Niezalogowano lub błędne dane logowania")

    if not path.exists(f"data/projects/{user[0]}/"):
        try:
            makedirs(f"data/projects/{user[0]}/")
        except Exception as ex:
            print(ex)
            raise HTTPException(status_code=500, detail="Nie można było utworzyc nowego projektu")

    uuid = uuid4()
    try:
        DBconn = sqlite3.connect(f"data/projects/{user[0]}/{uuid}.db")
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail="Nie można było utworzyc nowego projektu")
    DB = DBconn.cursor()

    DB.execute('''
    CREATE TABLE IF NOT EXISTS project_data (
        name TEXT NOT NULL
    );
    ''')

    DB.execute(f'''
    INSERT INTO project_data (name) VALUES
    ("{name}");
    ''')

    DB.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email TEXT NOT NULL
    );
    ''')

    DB.execute('''
    CREATE TABLE IF NOT EXISTS task (
        id INTEGER PRIMARY KEY,
        content TEXT,
        deadline REAL,
        status INT2 NOT NULL
    );
    ''')

    DB.execute('''
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        members JSON NOT NULL
    );
    ''')

    usersDB.execute(f'''
    UPDATE users SET projects = json_insert(projects, '$[#]', '{{"name":"{name}", "id":"{uuid}"}}')
    ''')

    # ''')
    DBconn.commit()
    usersDBconn.commit()
    DBconn.close()
    return { "message": "Pomyślnie utworzono nowy projekt." }

class ProjectDeletion(BaseModel):
    id: str

@app.post("/projects/delete")
async def delete_project(cookies: Annotated[Cookies, Cookie()], item: ProjectDeletion):
    user = getUser(cookies.email, cookies.hash)
    if not user:
        raise HTTPException(status_code=400, detail="Niezalogowano lub błędne dane logowania")

    if not path.exists(f"data/projects/{user[0]}/"):
        return { "message" : "Pomyślnie usunięto projekt." }

    if not path.exists(f"data/projects/{user[0]}/{item.id}.db"):
        return { "message" : "Pomyślnie usunięto projekt." }
    
    try:
        unlink(f"data/projects/{user[0]}/{item.id}.db")

        usersDB.execute(f'''
        UPDATE users
        SET projects = (
            SELECT json_group_array(value)
            FROM (
                SELECT value
                FROM json_each(projects)
                WHERE json_extract(value, '$.id') != '{item.id}'
            )
        )
        WHERE id = '{user[0]}';
        ''')
        usersDBconn.commit()

        return { "message" : "Pomyślnie usunięto projekt." }
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail="Nie udało się usunąć projektu")
