from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db
import sqlalchemy
from pydantic import BaseModel

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
        
        # if no user id is returned, the username already exists
        if result.rowcount < 1:
            id = -1
        else:
            id = result.one().user_id

    return {"user_id": id}

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
        
        # no matching username and password combination
        if result.rowcount < 1:
            id = -1
        else:
            id = result.one().user_id

    return {"user_id": id}