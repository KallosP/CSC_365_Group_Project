from fastapi import APIRouter, Depends 
from src.api import auth, user
from src import database as db
import sqlalchemy
from src.database import tasks_table as tasks, users_table as users, tags_table
from pydantic import BaseModel, validator, Field
from typing import List, Tuple
from datetime import time, datetime
import math

router = APIRouter(
    prefix="/scheduler",
    tags=["scheduler"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/suggest")
def suggest(user_id: int):


    # Logic: 
    #     - Assigns weights to priority and due_date fields. Tasks with a higher
    #       priority or closer due date have higher weights, those with lower
    #       priority/further due dates have lower weight.
    #     - Weights range from 0, 1, 2, or 3
    #     - Tasks with the highest weight are ordered first
    #     - Subtasks are created when a task can't fit into a time frame
    #     - Exhausting all timeframes means all tasks couldn't be completed
    #       in a day. If this is the case, then the remaining tasks are rolled
    #       over to the next day.

    with db.engine.begin() as connection:

        user.checkUser(user_id, connection)

        # Remove all subtasks from previous runs (prevent table clutter)
        connection.execute(sqlalchemy.text(
        """
        DELETE FROM subtasks
        WHERE user_id = :user_id
        """), [{"user_id": user_id}])

        # Get the user's availability (free time windows)
        result = connection.execute(sqlalchemy.text(
            """
            SELECT free_time
            FROM users
            WHERE user_id = :user_id
            """), [{"user_id": user_id}])
        free_time_windows = result.fetchone()[0]

        # Set the weights of each task. Order them further by due_date and estimated_time
        # due_date weights are based how close the due date is compared to the current time
        result = connection.execute(sqlalchemy.text(
        """
        SELECT task_id, name, priority, due_date, estimated_time,
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
        ORDER BY weight DESC, due_date, estimated_time
        """), [{"user_id": user_id}])

        # Store ordered tasks in list
        tasks = []
        for row in result:
            tasks.append(
                {
                    "task_id": row.task_id,
                    "name": row.name,
                    "priority": row.priority,
                    "due_date": row.due_date,
                    "estimated_time": row.estimated_time,
                    "weight": row.weight
                }
            )

        #print(tasks)

        schedule = []
        # Counter
        total_days = 0

        # Go through all tasks
        while(tasks):
            total_days += 1
            # Assign tasks to windows of free time
            for window in free_time_windows:
                # Convert the free time window to hours
                start = datetime.combine(datetime.today(), window[0])
                end = datetime.combine(datetime.today(), window[1])
                window_duration = (end - start).seconds / 3600
                #print("Frame: " + str(window[0]) + ", " + str(window[1]))

                # Iterate over a copy of tasks to not affect the indexes/ordering
                for task in tasks.copy():
                    
                    # estimated_time is required for this endpoint to work
                    if task["estimated_time"] is None:
                        return "ERROR: 1 or more tasks don't have estimated_time specified."

                    #print("Task: " + str(task["task_id"]))

                    task_work_duration = window_duration - task["estimated_time"]
                    # Current task can fit in time window
                    if task_work_duration >= 0:

                        # No more tasks can be assigned to this time frame, it's exhausted
                        window_duration -= task["estimated_time"]

                        # Add fields for clarity
                        task["day"] = total_days
                        task["free_time_range"] = [window[0], window[1]]

                        schedule.append(task)
                        # Remove the task to prevent duplicates
                        tasks.remove(task)

                        # Edge case: time frame is exhausted
                        if task_work_duration == 0:
                            # Continue to next time frame
                            break

                    # Current task cannot fit in time window
                    elif task_work_duration < 0:
                        # Create a subtask (split current task into two parts)
                        subtask = task.copy()
                        subtask["estimated_time"] = task["estimated_time"] - window_duration 
                        subtask["subtask"] = True
                        # Add subtask to front of tasks list (to maintain ordering)
                        tasks.insert(0, subtask)

                        # Insert the subtask into the subtasks table
                        connection.execute(sqlalchemy.text(
                            """
                            INSERT INTO subtasks (task_id, name, priority, due_date, estimated_time, weight, user_id)
                            VALUES (:task_id, :name, :priority, :due_date, :estimated_time, :weight, :user_id)
                            """), 
                            [{"task_id": subtask["task_id"], "name": subtask["name"], 
                            "priority": subtask["priority"], "due_date": subtask["due_date"], 
                            "estimated_time": subtask["estimated_time"], "weight": subtask["weight"], 
                            "user_id": user_id}])


                        # Add fields for clarity
                        task["day"] = total_days
                        task["free_time_range"] = [window[0], window[1]]

                        # Append first part of task to output list
                        schedule.append(task)
                        # Remove first part of task from tasks to avoid duplication
                        tasks.remove(task)
                        
                        # Window duration exhausted, go to next time frame
                        break

    return {"Suggested completion order": schedule}

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

@router.post("/set_free_time/{user_id}")
def suggest(user_id: int, free_time: FreeTime):

    # Convert tuple into a list (to make compatable with supabase column type)
    free_time_list = [[start_time, end_time] for start_time, end_time in free_time.free_time]

    # Update DB
    with db.engine.begin() as connection:

        user.checkUser(user_id, connection)

        try:
            # Explicitly lock user 
            connection.execute(sqlalchemy.text(
                """
                SELECT *
                FROM users
                WHERE user_id = :user_id
                FOR UPDATE
                """
            ), {"user_id": user_id}).fetchone()

            # Update user's free time while locked
            connection.execute(sqlalchemy.text(
                """
                UPDATE users
                SET free_time = :free_time
                WHERE user_id = :user_id
                """
                ), [{"free_time": free_time_list, "user_id": user_id}])
            
            # Commit transaction/release lock
            connection.commit()

            return "Successfully stored free time"
        
        except Exception as e:
            # Rollback transaction on error
            connection.rollback()
            return f"Error: {e}"