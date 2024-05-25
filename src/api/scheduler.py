from fastapi import APIRouter, Depends 
from src.api import auth
from src import database as db
import sqlalchemy
from sqlalchemy import Table, MetaData
from pydantic import BaseModel, validator, Field
from typing import List, Tuple
from datetime import time, datetime, timedelta
import heapq

router = APIRouter(
    prefix="/scheduler",
    tags=["scheduler"],
    dependencies=[Depends(auth.get_api_key)],
)

engine = db.engine
metadata = MetaData()

tasks = Table('tasks', metadata, autoload_with=db.engine)

@router.get("/suggest")
def suggest(user_id: int):

    # TODO: change how id is checked based on login/account creation is changed
    #if user_id < 0:
    #    "ERROR: Invalid login ID"

    # Logic: 
    #     - Assigns a weights to priority and due_date fields. Tasks with a higher
    #       priority or closer due date have higher weight, those with lower
    #       priority/further due dates have lower weight.
    #     - Weights are just 0, 1, 2, or 3; summed up = total weight
    #     - Tasks with the most weight are ordered first
    #     - TODO: incorporate the user's ranges of free time in ordering the tasks

    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT *,
                   (CASE
                        WHEN priority = 'high' THEN 3
                        WHEN priority = 'medium' THEN 2
                        WHEN priority = 'low' THEN 1
                        ELSE 0
                    END) +
                   (CASE
                        WHEN due_date <= NOW() THEN 3
                        WHEN due_date <= NOW() + INTERVAL '1 day' THEN 2
                        WHEN due_date <= NOW() + INTERVAL '2 days' THEN 1
                        ELSE 0
                    END) AS weight
            FROM tasks
            WHERE user_id = :user_id
            ORDER BY score DESC, due_date
            """), [{"user_id": user_id}])

        tasks = [dict(row._asdict()) for row in result]

    return tasks

class FreeTime(BaseModel):
    free_time: List[Tuple[time, time]] = Field(..., example=[("01:00", "11:59"), ("12:00", "23:59")])

    # Input validation
    @validator('free_time', each_item=True)
    def validate_time(cls, v):
        if v is None or len(v) != 2:
            raise ValueError('Invalid time range. Expected a tuple of two time objects.')
        start_time, end_time = v
        if start_time >= end_time:
            raise ValueError('Invalid time range. Start time must be before end time.')
        return v

users = Table('users', metadata, autoload_with=db.engine)

@router.post("/set_free_time/{user_id}")
def suggest(user_id: int, free_time: FreeTime):

    # Convert tuple into a list (to make compatable with supabase column type)
    free_time_list = [[start_time, end_time] for start_time, end_time in free_time.free_time]

    # Update DB
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            """
            UPDATE users
            SET free_time = :free_time
            WHERE user_id = :user_id
            """
            ), [{"free_time": free_time_list, "user_id": user_id}])

    return "Successfully stored free time"