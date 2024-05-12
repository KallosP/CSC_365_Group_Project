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
    type: str = None
    os: str = None
    repair: str = None
    task_id: int = 0

@router.post("/add")
def add_tag(tag: Tag):
    if user.login_id < 0:
        return "ERROR: Invalid login ID"
    
    with db.engine.begin() as connection:
        tag_id = connection.execute(sqlalchemy.text(
            """
            INSERT INTO tags (user_id, task_id, type, os, repair)
            VALUES
            (:user_id, :task_id, :type, :os, :repair)
            RETURNING tag_id
            """
            ), [{"user_id": user.login_id, "task_id": tag.task_id, "type": tag.type, "os": tag.os, 
                "repair": tag.repair}]).one().tag_id
    
    return {"task_id": tag_id}