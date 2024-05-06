from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db
import sqlalchemy
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/crud",
    tags=["crud"],
    dependencies=[Depends(auth.get_api_key)],
)

class Task(BaseModel):
    task_id: int
    name: str
    description: str
    priority: str
    status: str
    start_date: datetime.isoformat
    due_date: datetime.isoformat
    end_date: datetime.isoformat

@router.post("/create")
def create_task(task: Task):
    # TODO: Insert a task 
    # TODO: generate unique id 
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(""))
    return "OK"