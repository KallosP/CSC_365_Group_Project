from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db
import sqlalchemy
from pydantic import BaseModel
from datetime import datetime
import src.api.user as user

router = APIRouter(
    prefix="/crud",
    tags=["crud"],
    dependencies=[Depends(auth.get_api_key)],
)

class Task(BaseModel):
    # Required fields
    name: str

    # Optional
    description: str = None
    priority: str = None
    status: str = None
    start_date: datetime = None
    due_date: datetime = None
    end_date: datetime = None

@router.post("/create")
def create_task(task: Task):

    if user.login_id < 0:
        return "ERROR: Invalid login ID"
    
    with db.engine.begin() as connection:
        task_id = connection.execute(sqlalchemy.text(
            """
            INSERT INTO tasks (user_id, name, description, priority, status, start_date, due_date, end_date)
            VALUES
            (:user_id, :name, :description, :priority, :status, :start_date, :due_date, :end_date)
            RETURNING task_id
            """
            ), [{"user_id": user.login_id, "name": task.name, "description": task.description, "priority": task.priority,
                "status": task.status, "start_date": task.start_date, "due_date": task.due_date,
                "end_date": task.end_date}]).one().task_id
    
    return {"task_id": task_id}

@router.post("/read/{task_id}")
def read_task(task_id: int):

    if user.login_id < 0:
        return "ERROR: Invalid login ID"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT user_id, name, description, priority, status, start_date, due_date, end_date
            FROM tasks
            WHERE task_id = :task_id AND user_id = :user_id
            """
        ), [{"task_id": task_id, "user_id": user.login_id}])

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