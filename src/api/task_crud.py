from fastapi import APIRouter, Depends, HTTPException
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
    # NOTE: All fields are optional to allow flexibility in update_task
    
    name: str = None
    description: str = None
    priority: str = None
    status: str = None
    start_date: datetime = None
    due_date: datetime = None
    end_date: datetime = None
    estimated_time: int = None

# User input validation
def priorityIsValid (priority: str):
    return priority is None or priority.lower() in ["high", "medium", "low"]
def statusIsValid (status: str):
    return status is None or status.lower() in ["complete", "in progress", "not started"]

@router.post("/create")
def create_task(user_id: int, task: Task):

    if not priorityIsValid(task.priority):
        return "ERROR: priority field must match one of the following: 'high', 'medium', or 'low'"

    if not statusIsValid(task.status):
        return "ERROR: status field must match one of the following: 'complete', 'in progress', or 'not started'"
    
    with db.engine.begin() as connection:

        # Ensure task has a name
        if task.name == None:
            return "ERROR: Task must have name"

        task_id = connection.execute(sqlalchemy.text(
            """
            INSERT INTO tasks (user_id, name, description, priority, status, start_date, due_date, end_date, estimated_time)
            VALUES
            (:user_id, :name, :description, :priority, :status, :start_date, :due_date, :end_date, :estimated_time)
            RETURNING task_id
            """
            ), [{"user_id": user_id, "name": task.name, "description": task.description, "priority": task.priority,
                "status": task.status, "start_date": task.start_date, "due_date": task.due_date,
                "end_date": task.end_date, "estimated_time": task.estimated_time}]).one().task_id
    
    return {"task_id": task_id}

@router.post("/read")
def read_task(user_id: int, task_id: int):

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT name, description, priority, status, start_date, due_date, end_date, estimated_time
            FROM tasks
            WHERE task_id = :task_id AND user_id = :user_id
            """
        ), [{"task_id": task_id, "user_id": user_id}])

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
                "end_date": row.end_date,
                "estimated_time": row.estimated_time
            }

    return task

@router.post("/update")
def update_task(user_id: int, task_id: int, task: Task):

    if user_id < 0:
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
            end_date = COALESCE(:end_date, end_date),
            estimated_time = COALESCE(:estimated_time, estimated_time)
            WHERE task_id = :task_id AND user_id = :user_id
            RETURNING *
            """
        ), [{"task_id": task_id, "user_id": user_id, "name": task.name, 
             "description": task.description, "priority": task.priority, "status": task.status, 
             "start_date": task.start_date, "due_date": task.due_date, "end_date": task.end_date,
             "estimated_time": task.estimated_time}])
        
        if result.rowcount > 0:
            return "OK: Task successfully updated"

    return "ERROR: Task not found"


@router.post("/delete")
def delete_task(user_id: int, task_id: int):

    with db.engine.begin() as connection:
        # Delete the task
        result = connection.execute(
            sqlalchemy.text(
                """
                DELETE FROM tasks
                WHERE task_id = :task_id AND user_id = :user_id
                RETURNING task_id
                """
            ), [{"task_id": task_id, "user_id": user_id}]
        )

        # check if a task was deleted
        if result.rowcount > 0:
            #delete associated tags
            connection.execute(sqlalchemy.text(
                """
                DELETE FROM tags
                WHERE task_id = :task_id
                """
            ), {"task_id": task_id})

            return {"message": "OK: Task and associated tags successfully deleted"}
    
    return "ERROR: Task not found"
