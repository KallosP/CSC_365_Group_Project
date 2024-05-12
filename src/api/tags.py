from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db
import sqlalchemy
from pydantic import BaseModel
from datetime import datetime
import src.api.user as user

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    dependencies=[Depends(auth.get_api_key)],
)

class Tag(BaseModel):
    name: str = None

@router.post("{task_id}/add")
def add_tag(task_id: int, tag: Tag):
    if user.login_id < 0:
        return "ERROR: Invalid login ID"
    
    with db.engine.begin() as connection:

        # Check if task_id exists
        exists = connection.execute(sqlalchemy.text(
            """
            SELECT task_id
            FROM tasks
            WHERE task_id = :task_id
            """
            ), [{"task_id": task_id}]).fetchone()

        if exists == None:
            return "ERROR: task_id not found"

        connection.execute(sqlalchemy.text(
            """
            INSERT INTO tags (user_id, task_id, name)
            VALUES
            (:user_id, :task_id, :name)
            """
            ), [{"user_id": user.login_id, "task_id": task_id, "name": tag.name}])
    
    return {"OK"}