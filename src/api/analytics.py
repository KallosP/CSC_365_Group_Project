from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select, text
from src.database import metadata
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
        metadata.reflect(bind=connection)
        tasks_table = metadata.tables['tasks']

        # Query definition for the total # of tasks created
        total_tasks_query = select(func.count()).where(tasks_table.c.user_id == user_id)
        if start_date:
            total_tasks_query = total_tasks_query.where(tasks_table.c.start_date >= start_date)
        if end_date:
            total_tasks_query = total_tasks_query.where(tasks_table.c.start_date <= end_date)
        
        total_tasks = connection.execute(total_tasks_query).scalar()

        # Query for average completion time (in hours)
        avg_completion_time_query = select(func.avg(func.extract('epoch', tasks_table.c.end_date - tasks_table.c.start_date))).where(
            tasks_table.c.user_id == user_id,
            tasks_table.c.end_date.isnot(None),
            tasks_table.c.status == 'complete'
        )
        if start_date:
            avg_completion_time_query = avg_completion_time_query.where(tasks_table.c.start_date >= start_date)
        if end_date:
            avg_completion_time_query = avg_completion_time_query.where(tasks_table.c.end_date <= end_date)
        
        avg_completion_time_seconds = connection.execute(avg_completion_time_query).scalar()
        avg_completion_time = avg_completion_time_seconds / 3600 if avg_completion_time_seconds else 0

        # Overdue tasks count
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

        # Task status breakdown
        task_status_query = select(
            tasks_table.c.status,
            func.count().label('status_count')
        ).where(
            tasks_table.c.user_id == user_id
        ).group_by(tasks_table.c.status)
        
        task_statuses_result = connection.execute(task_status_query)
        task_statuses = {row['status']: row['status_count'] for row in task_statuses_result.mappings()}

        # Priority distribution
        priority_distribution_query = select(
            tasks_table.c.priority,
            func.count().label('priority_count')
        ).where(
            tasks_table.c.user_id == user_id
        ).group_by(tasks_table.c.priority)
        
        priority_distribution_result = connection.execute(priority_distribution_query)
        priority_distribution = {row['priority']: row['priority_count'] for row in priority_distribution_result.mappings()}

        # Return results
        return {
            "total_tasks": total_tasks,
            "avg_completion_time_hours": avg_completion_time,
            "overdue_tasks": overdue_tasks,
            "task_status_breakdown": task_statuses,
            "priority_distribution": priority_distribution,
        }

