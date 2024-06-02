from fastapi import APIRouter, Depends, HTTPException
from src.api import auth, user
from src import database as db
import sqlalchemy
from pydantic import BaseModel

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    dependencies=[Depends(auth.get_api_key)],
)

class Tag(BaseModel):
    name: str = None

@router.post("/add")
def add_tag(user_id: int, task_id: int, tag: Tag):
    """
    Adds a tag to task associated with user_id and task_id

    Returns HTTP status
    """
    
    with db.engine.begin() as connection:

        user.checkUser(user_id, connection)

        # Check if task_id exists and lock it
        exists = connection.execute(sqlalchemy.text(
            """
            SELECT task_id
            FROM tasks
            WHERE task_id = :task_id AND user_id = :user_id
            FOR UPDATE
            """
            ), {"task_id": task_id, "user_id": user_id}).fetchone()

        if exists is None:
            raise HTTPException(status_code=404, detail="Task not found for user")
        
        # Check if we already have a tag of the same name for a given task and lock existing tags
        tag_exists = connection.execute(sqlalchemy.text(
            """
            SELECT tag_id
            FROM tags
            WHERE task_id = :task_id AND user_id = :user_id AND name = :tag
            FOR UPDATE
            """
            ), {"task_id": task_id, "user_id": user_id, "tag": tag.name}).fetchone()
        
        if tag_exists:
            raise HTTPException(status_code=409, detail="Tag already exists for task")

        # Insert the new tag
        connection.execute(sqlalchemy.text(
            """
            INSERT INTO tags (user_id, task_id, name)
            VALUES (:user_id, :task_id, :name)
            """
            ), {"task_id": task_id, "user_id": user_id, "name": tag.name})
    
    return "OK"


@router.get("/get")
def get_tags(user_id: int, task_id: int):
    """
    Retrieves all tags associated with task

    Returns list of tags
    """

    with db.engine.begin() as connection:

        user.checkUser(user_id, connection)

        # Check if task_id exists
        exists = connection.execute(sqlalchemy.text(
            """
            SELECT task_id
            FROM tasks
            WHERE task_id = :task_id AND user_id = :user_id
            """
            ), [{"task_id": task_id, "user_id": user_id}]).fetchone()
        
        if exists is None:
            raise HTTPException(status_code=404, detail="Task not found for user")
        
        tags = connection.execute(sqlalchemy.text(
            """
            SELECT DISTINCT name
            FROM tags
            WHERE task_id = :task_id AND user_id = :user_id
            """
            ), [{"task_id": task_id, "user_id": user_id}])
        
        result = []
        for tag in tags:
            result.append(tag[0])
        return {
                "tags": result
                }
    
class Tags(BaseModel):
    names: list[str] = None


@router.delete("/remove")
def remove_tag(user_id: int, task_id: int, tags: Tags):
    """
    Removes matching tags from task contained in tags argument

    Returns HTTP status
    """

    with db.engine.begin() as connection:

        user.checkUser(user_id, connection)

        # Check if task_id exists
        exists = connection.execute(sqlalchemy.text(
            """
            SELECT task_id
            FROM tasks
            WHERE task_id = :task_id AND user_id = :user_id
            """
            ), [{"task_id": task_id, "user_id": user_id}]).fetchone()

        if exists is None:
            raise HTTPException(status_code=404, detail="Task not found for user")
        
        deleted = connection.execute(sqlalchemy.text(
            """
            DELETE FROM tags
            WHERE task_id = :task_id AND user_id = :user_id
            AND name IN :names
            """
            ), [{"task_id": task_id, "user_id": user_id, "names": tuple(tags.names)}])
        
        if deleted.rowcount <= 0:
            raise HTTPException(status_code=404, detail="Could not delete, tag not found.")
        
    return "OK: Tag successfully removed"
