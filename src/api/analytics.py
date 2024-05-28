from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Table, MetaData, func, select
from datetime import datetime
from typing import Optional
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("")
def analytics(
    user_id: int, 
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):

    with db.engine.begin() as connection:
        metadata = MetaData()
        metadata.reflect(bind=connection)
        tasks_table = metadata.tables['tasks']

        # Query definition for the total # of tasks created
        total_tasks_query = select(func.count()).where(
            tasks_table.c.user_id == user_id
        )
        if start_date:
            total_tasks_query = total_tasks_query.where(tasks_table.c.start_date >= start_date)
        if end_date:
            total_tasks_query = total_tasks_query.where(tasks_table.c.start_date <= end_date)
        
        total_tasks = connection.execute(total_tasks_query).scalar()

        # Query for average completion time (in hours)
        avg_completion_time_query = select(func.avg(func.extract('epoch', tasks_table.c.end_date - tasks_table.c.start_date))).where(
            tasks_table.c.user_id == user_id,
            tasks_table.c.end_date.isnot(None)
        )
        if start_date:
            avg_completion_time_query = avg_completion_time_query.where(tasks_table.c.start_date >= start_date)
        if end_date:
            avg_completion_time_query = avg_completion_time_query.where(tasks_table.c.end_date <= end_date)
        
        avg_completion_time_seconds = connection.execute(avg_completion_time_query).scalar()
        avg_completion_time = None
        if avg_completion_time_seconds:
            avg_completion_time = avg_completion_time_seconds / 3600

        # Overdue tasks (if applicable to the user / timeframe)
        overdue_tasks_query = select(func.count()).where(
            tasks_table.c.user_id == user_id,
            tasks_table.c.due_date < func.now(),
            tasks_table.c.end_date.is_(None)
        )
        if start_date:
            overdue_tasks_query = overdue_tasks_query.where(tasks_table.c.due_date >= start_date)
        if end_date:
            overdue_tasks_query = overdue_tasks_query.where(tasks_table.c.due_date <= end_date)
        
        overdue_tasks = connection.execute(overdue_tasks_query).scalar()

        # Add more queries for other metrics as needed.

        return {
            "total_tasks": total_tasks if total_tasks is not None else 0,
            "avg_completion_time_hours": avg_completion_time if avg_completion_time is not None else 0,
            "overdue_tasks": overdue_tasks if overdue_tasks is not None else 0,
            # Add more metrics as needed.
        }
