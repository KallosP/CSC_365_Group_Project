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
    # NOTE: All fields are optional to allow flexibility in update_task
    
    name: str = None
    description: str = None
    priority: str = None
    status: str = None
    start_date: datetime = None
    due_date: datetime = None
    end_date: datetime = None

def priorityIsValid (priority: str):
    return priority is None or priority.lower() in ["high", "medium", "low"]
           
def statusIsValid (status: str):
    return status is None or status.lower() in ["complete", "in progress", "not started"]

@router.post("/create")
def create_task(task: Task):

    if user.login_id < 0:
        return "ERROR: Invalid login ID"

    if not priorityIsValid(task.priority):
        return "ERROR: priority field must match one of the following: 'high', 'medium', or 'low'"

    if not statusIsValid(task.status):
        return "ERROR: status field must match one of the following: 'complete', 'in progress', or 'not started'"
    
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
            SELECT name, description, priority, status, start_date, due_date, end_date
            FROM tasks
            WHERE task_id = :task_id AND user_id = :user_id
            """
        ), [{"task_id": task_id, "user_id": user.login_id}])

        # check if task id in table
        task = {}
        if result.rowcount > 0:
            row = result.one()
            task = {
                "name": row.name,
                "description": row.description,
                "priority": row.priority,
                "status": row.status,
                "start_date": row.start_date,
                "due_date": row.due_date,
                "end_date": row.end_date
            }

    return task

@router.post("/update/{task_id}")
def update_task(task_id: int, task: Task):

    if user.login_id < 0:
        return "ERROR: Invalid login ID"

    if not priorityIsValid(task.priority):
        return "ERROR: priority field must match one of the following: 'high', 'medium', or 'low'"

    if not statusIsValid(task.status):
        return "ERROR: status field must match one of the following: 'complete', 'in progress', or 'not started'"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            UPDATE tasks SET 
            name = COALESCE(:name, name),
            description = COALESCE(:description, description),
            priority = COALESCE(:priority, priority),
            status = COALESCE(:status, status),
            start_date = COALESCE(:start_date, start_date),
            due_date = COALESCE(:due_date, due_date),
            end_date = COALESCE(:end_date, end_date)
            WHERE task_id = :task_id AND user_id = :user_id
            RETURNING *
            """
        ), [{"task_id": task_id, "user_id": user.login_id, "name": task.name, 
             "description": task.description, "priority": task.priority, "status": task.status, 
             "start_date": task.start_date, "due_date": task.due_date, "end_date": task.end_date}])
        
        if result.rowcount > 0:
            return "OK"

    return "ERROR: Task not found"


@router.post("/delete/{task_id}")
def delete_task(task_id: int):

    if user.login_id < 0:
        return "ERROR: Invalid login ID"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            DELETE FROM tasks
            WHERE task_id = :task_id AND user_id = :user_id
            RETURNING *
            """
        ), [{"task_id": task_id, "user_id": user.login_id}])

        # check if a task was deleted
        if result.rowcount > 0:
            return "OK"
    
    return "ERROR: Task not found"