from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db
import sqlalchemy
from sqlalchemy import create_engine, Table, MetaData
from enum import Enum
import src.api.user as user
import os

router = APIRouter(
    prefix="/sort",
    tags=["sort"],
    dependencies=[Depends(auth.get_api_key)],
)

class sort_options(str, Enum):
    name = "name"
    priority = "priority"
    status = "status"
    start_date = "start_date"
    due_date = "due_date"
    end_date = "end_date"

class sort_order(str, Enum):
    asc = "asc"
    desc = "desc"   

engine = db.engine
metadata = MetaData()

tasks = Table('tasks', metadata, autoload_with=engine)

@router.get("/")
def sort(sort_col: sort_options = sort_options.due_date,
                sort_order: sort_order = sort_order.desc):
    """
    sort_col = which columns to sort by
    sort_order = direction of sort
    Default = sort by due_date in descending order
    """
    
    # Check for valid user
    if user.login_id < 0:
        return "ERROR: Invalid login ID"

    # TODO: change sorting of priority and status from being alphabetic 

    if sort_col is sort_options.name:
        order_by_col = tasks.c.name
    elif sort_col is sort_options.priority:
        order_by_col = tasks.c.priority
    elif sort_col is sort_options.status:
        order_by_col = tasks.c.status
    elif sort_col is sort_options.start_date:
        order_by_col = tasks.c.start_date
    elif sort_col is sort_options.due_date:
        order_by_col = tasks.c.due_date
    elif sort_col is sort_options.end_date:
        order_by_col = tasks.c.end_date
    else:  
        assert False

    if sort_order is sort_order.asc:
        order_by = sqlalchemy.asc(order_by_col)
    else:  # default is desc
        order_by = sqlalchemy.desc(order_by_col)
        
    # Construct the query
    stmt = (
        sqlalchemy.select(
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
        .where(tasks.c.user_id == user.login_id)
        .order_by(order_by, order_by_col)
    )

    # Execute the query
    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        json = []
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


    return {"results": json}

tags_table = Table('tags', metadata, autoload_with=engine)

@router.get("/tags")
def sort_by_tags(tag: str):
    
    # Check for valid user
    if user.login_id < 0:
        return "ERROR: Invalid login ID"

    # Logic: Query all tasks that have the given tag, append them first
    #        to the json object. Then append the rest of the tasks that
    #        don't have the given tag to the json. 

   # Query for tasks with given tag
    stmt_with_tag = (
        sqlalchemy.select(
            tags_table.c.name.label("tag_name"),
            tasks.c.task_id,
            tasks.c.name.label("task_name"),
            tasks.c.description,
            tasks.c.priority,
            tasks.c.status,
            tasks.c.start_date,
            tasks.c.due_date,
            tasks.c.end_date
        )
        .select_from(tasks)
        .join(tags_table, tasks.c.task_id == tags_table.c.task_id)
        .where(tasks.c.user_id == user.login_id)
        .where(tags_table.c.name == tag)
    )

    # Query for tasks that do not have given tag
    stmt_without_tag = (
        sqlalchemy.select(
            tags_table.c.name.label("tag_name"),
            tasks.c.task_id,
            tasks.c.name.label("task_name"),
            tasks.c.description,
            tasks.c.priority,
            tasks.c.status,
            tasks.c.start_date,
            tasks.c.due_date,
            tasks.c.end_date
        )
        # Only select each task once
        .distinct(tasks.c.task_id)
        .select_from(tasks)
        .outerjoin(tags_table, tasks.c.task_id == tags_table.c.task_id)
        .where(tasks.c.user_id == user.login_id)
        .where(sqlalchemy.not_(tags_table.c.name == tag))
    )

    json = []

    # Execute query with tag
    with db.engine.connect() as conn:
        result = conn.execute(stmt_with_tag)
        for row in result:
            json.append(
                {
                    "sorted_by_tag": row.tag_name,
                    "task_id": row.task_id,
                    "name": row.task_name,
                    "description": row.description,
                    "priority": row.priority,
                    "status": row.status,
                    "start_date": row.start_date,
                    "due_date": row.due_date,
                    "end_date": row.end_date
                }
            )

        # Execute query without tag
        result = conn.execute(stmt_without_tag)
        for row in result:
            json.append(
                {
                    # Exclude display of tag
                    "task_id": row.task_id,
                    "name": row.task_name,
                    "description": row.description,
                    "priority": row.priority,
                    "status": row.status,
                    "start_date": row.start_date,
                    "due_date": row.due_date,
                    "end_date": row.end_date
                }
            )
 
    return {"results": json}
