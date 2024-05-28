from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db
import sqlalchemy
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
import src.api.user as user

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
    # NOTE: All fields are optional to allow flexibility in update_task
    
    name: str = None
    description: str = None
    start_date: datetime = None
    due_date: datetime = None
    end_date: datetime = None
    estimated_time: int = None


@router.post("/create")
def create_task(task: Task, priority: PriorityEnum = PriorityEnum.low, status: StatusEnum = StatusEnum.not_started):

    if user.login_id < 0:
        raise HTTPException(status_code=400, detail="Invalid login ID")
    
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
<<<<<<< HEAD:src/api/task.py
            ), [{"user_id": user.login_id, "name": task.name, "description": task.description, "priority": priority,
                "status": status, "start_date": task.start_date, "due_date": task.due_date,
                "end_date": task.end_date}]).one().task_id
=======
            ), [{"user_id": user.login_id, "name": task.name, "description": task.description, "priority": task.priority,
                "status": task.status, "start_date": task.start_date, "due_date": task.due_date,
                "end_date": task.end_date, "estimated_time": task.estimated_time}]).one().task_id
>>>>>>> main:src/api/task_crud.py
    
    return {"task_id": task_id}

@router.get("/read/{task_id}")
def read_task(task_id: int):

    if user.login_id < 0:
        raise HTTPException(status_code=400, detail="Invalid login ID")

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT name, description, priority, status, start_date, due_date, end_date, estimated_time
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
                "end_date": row.end_date,
                "estimated_time": row.estimated_time
            }

    return task

@router.patch("/update/{task_id}")
def update_task(task_id: int, task: Task, priority: PriorityEnum = None, status: StatusEnum = None):

    if user.login_id < 0:
        raise HTTPException(status_code=400, detail="Invalid login ID")

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
        ), [{"task_id": task_id, "user_id": user.login_id, "name": task.name, 
<<<<<<< HEAD:src/api/task.py
             "description": task.description, "priority": priority, "status": status, 
             "start_date": task.start_date, "due_date": task.due_date, "end_date": task.end_date}])
=======
             "description": task.description, "priority": task.priority, "status": task.status, 
             "start_date": task.start_date, "due_date": task.due_date, "end_date": task.end_date,
             "estimated_time": task.estimated_time}])
>>>>>>> main:src/api/task_crud.py
        
        if result.rowcount > 0:
            return "OK: Task successfully updated"

    raise HTTPException(status_code=404, detail="Task not found")


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
            #delete associated tags
            connection.execute(sqlalchemy.text(
                """
                DELETE FROM tags
                WHERE task_id = :task_id
                """
            ), {"task_id": task_id})

<<<<<<< HEAD:src/api/task.py
            return "OK: Task and associated tags successfully deleted"
    
    raise HTTPException(status_code=404, detail="Task not found")
=======
            return {"message": "OK: Task and associated tags successfully deleted"}
    
    return "ERROR: Task not found"
>>>>>>> main:src/api/task_crud.py
