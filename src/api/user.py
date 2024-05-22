from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db
import sqlalchemy
from pydantic import BaseModel

login_id = -1

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    user_name: str
    password: str

@router.post("/create")
def create_user(user: User):

    # NOTE: If a user already exists nothing is inserted

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
        
        global login_id
        if result.rowcount > 0:
            login_id = result.one().user_id
        else:
            login_id = -1
            return "ERROR: Username already exists"

    return {"user_id": login_id}

@router.post("/login")
def login(user: User):

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT user_id
            FROM users
            WHERE user_name LIKE :user_name AND password LIKE :password
            LIMIT 1
            """
            ), [{"user_name": user.user_name, "password": user.password}])
    
        global login_id
        if result.rowcount > 0:
            login_id = result.one().user_id
        else:
            login_id = -1
            return "ERROR: Incorrect username or password"

    return "OK: Successfully logged in"

@router.post("/logout")
def logout():

    global login_id
    if login_id == -1:
        return "ERROR: Not logged in"
    else:
        login_id = -1
        return "OK: Successfully logged out"
