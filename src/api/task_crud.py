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
    user_id: int
    name: str
    description: str
    priority: str
    status: str
    start_date: datetime
    due_date: datetime
    end_date: datetime

@router.post("/create")
def create_task(task: Task):

    # TODO: need to make a user account creation and have their unique ID tied to all the tasks they create

    with db.engine.begin() as connection:
        task_id = connection.execute(sqlalchemy.text(
            """
            INSERT INTO tasks (user_id, name, description, priority, status, start_date, due_date, end_date)
            VALUES
            (:user_id, :name, :description, :priority, :status, :start_date, :due_date, :end_date)
            RETURNING task_id
            """
            ), [{"user_id": task.user_id, "name": task.name, "description": task.description, "priority": task.priority,
                "status": task.status, "start_date": task.start_date, "due_date": task.due_date,
                "end_date": task.end_date}]).one().task_id
    
    return {"task_id": task_id}

@router.post("/read/{task_id}")
def read_task(task_id: int):

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT user_id, name, description, priority, status, start_date, due_date, end_date
            FROM tasks
            WHERE task_id = :task_id
            """
        ), [{"task_id": task_id}])

        # check if task id in table
        task = {}
        if result.rowcount > 0:
            row = result.one()
            task = {
                "user_id": row.user_id,
                "name": row.name,
                "description": row.description,
                "priority": row.priority,
                "status": row.status,
                "start_date": row.start_date,
                "due_date": row.due_date,
                "end_date": row.end_date
            }

    return task