from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db
import sqlalchemy
from pydantic import BaseModel

router = APIRouter(
    prefix="/sort",
    tags=["sort"],
    dependencies=[Depends(auth.get_api_key)],
)

# TODO: sort by all fields except description

@router.post("/sort")
def create_user():

    # NOTE: If a user already exists nothing is inserted

    #with db.engine.begin() as connection:
    #    result = connection.execute(sqlalchemy.text()) 

    return "OK"