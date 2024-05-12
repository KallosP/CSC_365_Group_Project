from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db
import sqlalchemy
from sqlalchemy import create_engine, Table, MetaData
from pydantic import BaseModel
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

db_uri = os.getenv('POSTGRES_URI')
engine = create_engine(db_uri)
metadata = MetaData()

tasks = Table('tasks', metadata, autoload_with=engine)

@router.post("/sort")
def create_user(sort_col: sort_options = sort_options.due_date,
                sort_order: sort_order = sort_order.desc):
    """
    sort_col = which columns to sort by
    sort_order = direction of sort
    Default = sort by due_date in descending order
    """
    
    # Check for valid user
    if user.login_id < 0:
        return "ERROR: Invalid login ID"

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