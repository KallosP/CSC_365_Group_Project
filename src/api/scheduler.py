from fastapi import APIRouter, Depends, HTTPException
from src.api import auth
from src import database as db
import sqlalchemy
from sqlalchemy import Table, MetaData, select
from pydantic import BaseModel

router = APIRouter(
    prefix="/scheduler",
    tags=["scheduler"],
    dependencies=[Depends(auth.get_api_key)],
)

engine = db.engine
metadata = MetaData()

# Reflect existing tables
users = Table('users', metadata, autoload_with=db.engine)
tasks = Table('tasks', metadata, autoload_with=db.engine)

#TODO:
#  - user availability - columns in the user table w/ amount of time spent working and free time
#  - estimated time to complete
#  - add conflict resolution for conflicting tasks (rearrange tasks to different days/times, notify user of change)
#  - sort the tasks to be most optimal order of completion based on user break time/work time and other features
@router.get("/suggest")
def suggest(user_id: int):

    # TODO: change how id is checked based on login/account creation is changed
    if user_id < 0:
        return "ERROR: Invalid login ID"
    
    json = []

    # TODO: Orders by priority and due date, basic start 
    #       - need to add columns for: estimated time to complete and user availability
    #       - find the most optimal order in which the tasks should be done using
    #           due date, priority, time to complete, and user availability
    stmt = (
        select(
            tasks.c.task_id,
            tasks.c.name,
            tasks.c.description,
            tasks.c.priority,
            tasks.c.status,
            tasks.c.start_date,
            tasks.c.due_date,
            tasks.c.end_date
        )
        .select_from(tasks)
        .where(tasks.c.user_id == user_id).order_by(tasks.c.priority, tasks.c.due_date)
    )
    
    # Execute the query
    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            json.append(
                {
                    "task_id": row.task_id,
                    "name": row.name,
                    "description": row.description,
                    "priority": row.priority,
                    "status": row.status,
                    "start_date": row.start_date,
                    "due_date": row.due_date,
                    "end_date": row.end_date
                }
            )

    return json