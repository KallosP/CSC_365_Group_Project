from fastapi import APIRouter, Depends, HTTPException
from src.api import auth
from src import database as db
import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import Connection

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)
def checkUser(user_id: int, connection: Connection):
    try:
        # Try to return one row
        connection.execute(sqlalchemy.text(
            """
            SELECT user_id 
            FROM users
            WHERE user_id = :user_id
            """
        ), [{"user_id": user_id}]).one()
    except: 
        raise HTTPException(status_code=404, detail="Invalid user ID")

class User(BaseModel):
    user_name: str
    password: str

@router.post("/create")
def create_user(user: User):
    """
    Add to username and password to user table.
    If a user already exists nothing is inserted

    Returns user id into users table
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            INSERT INTO users 
            (user_name, password)
            SELECT :user_name, :password
            WHERE :user_name NOT IN (SELECT user_name FROM users)
            RETURNING user_id
            """
            ), [{"user_name": user.user_name, "password": user.password}])
        
        if result.rowcount > 0:
            user_id = result.one().user_id
        else:
            raise HTTPException(status_code=409, detail="Username already exists")

    return {"user_id": user_id}

@router.post("/get_user_id")
def get_user_id(user: User):
    """
    Matches username and password to id in users table

    Returns user id into users table
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT user_id
            FROM users
            WHERE user_name LIKE :user_name AND password LIKE :password
            LIMIT 1
            """
            ), [{"user_name": user.user_name, "password": user.password}])
    
        if result.rowcount > 0:
            user_id = result.one().user_id
        else:
            raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"user_id": user_id}

