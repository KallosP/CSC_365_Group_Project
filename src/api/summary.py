from fastapi import APIRouter, Depends, HTTPException
from src.api import auth, user
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/summary",
    tags=["summary"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/")
def summary(user_id: int):
    """
    Retrieves count of tasks for user grouped by status

    Returns dictionary of task counts grouped by status
    """

    # Fetch summary info from db
    with db.engine.begin() as connection:

        user.checkUser(user_id, connection)

        result = connection.execute(sqlalchemy.text(
            """
            WITH status_counts AS (
                SELECT status, COALESCE(COUNT(*), 0) AS num_tasks
                FROM tasks
                WHERE user_id = :user_id
                GROUP BY status
            ),
            total_tasks AS (
                SELECT COALESCE(COUNT(*), 0) AS num_tasks
                FROM tasks
                WHERE user_id = :user_id
            )
            SELECT 
                total_tasks.num_tasks AS total,
                COALESCE(s1.num_tasks,0) AS complete, 
                COALESCE(s2.num_tasks,0) AS in_progress, 
                COALESCE(s3.num_tasks,0) AS not_started
            FROM total_tasks
            LEFT JOIN status_counts AS s1 ON s1.status LIKE 'complete'
            LEFT JOIN status_counts AS s2 ON s2.status LIKE 'in progress'
            LEFT JOIN status_counts AS s3 ON s3.status LIKE 'not started'
            """
            ), [{"user_id": user_id}]).one()
    
    return  {
                "number_of_tasks": result.total,
                "tasks_completed": result.complete,
                "tasks_in_progress": result.in_progress,
                "tasks_not_started": result.not_started
            }
