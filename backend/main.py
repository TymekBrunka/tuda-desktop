import sqlite3
from typing import Annotated
from fastapi import FastAPI, HTTPException, exceptions
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from hashlib import sha256
import re

from shared import *

try:
    usersDBconn = sqlite3.connect("data/users.db")
except Exception as ex:
    print(ex)
    exit()
usersDB = usersDBconn.cursor()

usersDB.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    projects JSON
);
''')
usersDBconn.commit()

class Cookies(BaseModel):
    email: str
    hash: str

@app.get("/")
async def root():
    raise HTTPException(status_code=400, detail="Hello World")

class RegisterModel(BaseModel):
    name: str
    surname: str
    email: str
    password: str

@app.post("/users/register/")
async def register(data: RegisterModel):
    """ kopiowanie danych do sanityzacji przed wstrzykiwaniem sql'a """
    name: str = data.name[:]
    surname: str = data.surname[:]
    email: str = data.email[:]
    password: str = data.password[:]

    name.replace('"', "").replace("\\", "")
    surname.replace('"', "").replace("\\", "")
    email.replace('"', "").replace("\\", "")
    password.replace('"', '\\"').replace("\\", "\\\\") #hasła muszą być bezpieczne, a jak chodzi o resztę to jak ktoś może mieć \ i " w imieniu ?

    if len(name) < 3 or len(surname) < 3:
        raise HTTPException(status_code=400, detail="Imię lub nazwisko za krótkie.")
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Hasło jest za krótkie.")
    if not re.fullmatch(r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-z-A-Z]{2,}$", email):
        raise HTTPException(status_code=400, detail="Niepoprawny email.")

    usersDB.execute('''
    SELECT * from users WHERE name = ? AND surname = ? LIMIT 1;
    ''', (
        name,
        surname
    ))
    user = usersDB.fetchone()

    if user: #czy jest osoba o podanum imieniu i nazwisku
        return { "message": f"{name} {surname} już jest zarejestrowany(/a)." }

    try:
        hash = sha256()
        hash.update((password[4:7] + password + password[2:4]).encode())
        password = hash.hexdigest()
        usersDB.execute('''
        INSERT INTO users (name, surname, email, password, projects) VALUES (?, ?, ?, ?, ?);
        ''', (
            name,
            surname,
            email,
            password,
            "[]"
        ))
        usersDBconn.commit();
    except:
        raise HTTPException(status_code=500, detail="Błąd rejestracji (nasza wina)")
    return { "message": f"Pomyślnie zarejestrowano {name} {surname}" }

class LoginModel(BaseModel):
    email: str
    password: str

@app.post("/users/login/")
async def login(data: LoginModel):
    """ kopiowanie danych do sanityzacji przed wstrzykiwaniem sql'a """
    email: str = data.email[:]
    password: str = data.password[:]

    email.replace('"', "").replace("\\", "")
    password.replace('"', '\\"').replace("\\", "\\\\") #hasła muszą być bezpieczne, a jak chodzi o resztę to jak ktoś może mieć \ i " w imieniu ?

    hash = sha256()
    hash.update((password[4:7] + password + password[2:4]).encode())
    password = hash.hexdigest()

    user = getUser(email, password)

    if user: #czy jest osoba o podanum imieniu i nazwisku
        content = { "message": f"Pomyslnie zalogowano" }
        response = JSONResponse(content=content)
        response.set_cookie(key="email", value=email)
        response.set_cookie(key="hash", value=password)
        return response
    else:
        raise HTTPException(status_code=400, detail="Email lub hasło niepoprawne.")

import api.projects_general
import api.groups_general
# usersDBconn.close() #zkomentowane bo fastapi nigdy się nie zamyka a to zamyka bazę pred nim
