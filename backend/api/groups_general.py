import sqlite3
from sys import exception
from typing import Annotated
from fastapi import FastAPI, HTTPException, Cookie, exceptions
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from hashlib import sha256
from uuid import uuid4

from shared import *

class AddingMember(BaseModel):
    owner_id: int
    project_id: int
    user_id: int

@app.post("/members/add/")
async def add_project_member(item: AddingMember, cookies: Annotated[Cookies, Cookie()]):
    user = getUser(cookies.email, cookies.hash)
    if (not user):
        return

    if user[0] == item.user_id:
        return

    if user[0] != item.owner_id:
        return

    DBconn = sqlite3.connect(f"data/projects/{user[0]}/{item.project_id}.db")
    DB = DBconn.cursor()
    DB.execute(f'''
    SELECT json_group_array(value)
    FROM (
        SELECT value
        FROM json_each(users)
        WHERE json_extract(value, '$.id') == '{item.user_id}'
    );
    ''')
    memberOrNull = DB.fetchone()

    if memberOrNull:
        return

    usersDB.execute(f'''
    SELECT * from users WHERE id = {item.user_id};
    ''')
    memberFrThisTime = usersDB.fetchone()

    DB.execute(f'''
    INSERT INTO users values (?, ?, ?, ?) 
    ''', (
        memberFrThisTime[0],
        memberFrThisTime[1],
        memberFrThisTime[2],
        memberFrThisTime[3]
    ));
