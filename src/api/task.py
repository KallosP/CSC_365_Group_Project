from fastapi import APIRouter, Depends, HTTPException
from src.api import auth
from src import database as db
import sqlalchemy
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

router = APIRouter(
    prefix="/task",
    tags=["task"],
    dependencies=[Depends(auth.get_api_key)],
)

class StatusEnum(str, Enum):
    complete = "complete"
    in_progress = "in progress"
    not_started = "not started"

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(BaseModel):
    # NOTE: All attributes are optional to allow flexibility in update_task
    
    name: str = None
    description: str = None
    start_date: datetime = None
    due_date: datetime = None
    end_date: datetime = None
    estimated_time: int = None


@router.post("/create")
def create_task(user_id: int, task: Task, priority: PriorityEnum = None, status: StatusEnum = None):
    """
    Creates new task in tasks table. 
    All attributes are optional except task name

    Returns task id into tasks table
    """

    with db.engine.begin() as connection:

        # Ensure task has a name
        if task.name == None or task.name == '':
            raise HTTPException(status_code=400, detail="Task must have a name")

        task_id = connection.execute(sqlalchemy.text(
            """
            INSERT INTO tasks (user_id, name, description, priority, status, start_date, due_date, end_date, estimated_time)
            VALUES
            (:user_id, :name, :description, :priority, :status, :start_date, :due_date, :end_date, :estimated_time)
            RETURNING task_id
            """
            ), [{"user_id": user_id, "name": task.name, "description": task.description, "priority": priority,
                "status": status, "start_date": task.start_date, "due_date": task.due_date,
                "end_date": task.end_date, "estimated_time": task.estimated_time}]).one().task_id
    
    return {"task_id": task_id}

@router.get("/read")
def read_task(user_id: int, task_id: int):
    """
    Reads corresponding task attributes for matching user_id and task_id

    Returns dictionary of attributes for task
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT name, description, priority, status, start_date, due_date, end_date, estimated_time
            FROM tasks
            WHERE task_id = :task_id AND user_id = :user_id
            """
        ), [{"task_id": task_id, "user_id": user_id}])

        # check if task id in table
        if result.rowcount > 0:
            row = result.one()
            return {
                "name": row.name,
                "description": row.description,
                "priority": row.priority,
                "status": row.status,
                "start_date": row.start_date,
                "due_date": row.due_date,
                "end_date": row.end_date,
                "estimated_time": row.estimated_time
            }
        
    raise HTTPException(status_code=404, detail="Task not found for user")


@router.put("/update")
def update_task(user_id: int, task_id: int, task: Task, priority: PriorityEnum = None, status: StatusEnum = None):
    """
    Updates non-null task attributes for a matching user_id and task_id

    Returns HTTP status
    """

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
             "description": task.description, "priority": priority, "status": status, 
             "start_date": task.start_date, "due_date": task.due_date, "end_date": task.end_date,
             "estimated_time": task.estimated_time}])
        
        if result.rowcount > 0:
            return "OK: Task successfully updated"

    raise HTTPException(status_code=404, detail="Task not found for user")


@router.delete("/delete")
def delete_task(user_id: int, task_id: int):
    """
    Removes a task and all tags associated with task for a matching user_id and task_id

    Returns HTTP status
    """

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

            return "OK: Task and associated tags successfully deleted"
    
    raise HTTPException(status_code=404, detail="Task not found for user")
