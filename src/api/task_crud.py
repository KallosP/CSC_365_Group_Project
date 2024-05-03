from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/crud",
    tags=["crud"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/plan")
def create_task():
    # TODO: Insert a task 
    #with db.engine.begin() as connection:

    return "OK"