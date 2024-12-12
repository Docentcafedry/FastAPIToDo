from fastapi import APIRouter, HTTPException, Path
from starlette import status
from depends.db import db_connection
from depends.auth import current_user_dependency
from models import Todo
from sqlalchemy import select
from schemas import TodoUpdate

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_todos(db: db_connection, current_user: current_user_dependency):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You have no rights to browse this resource")
    todos = db.scalars(select(Todo).order_by(Todo.id)).all()
    return todos


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_connection, current_user: current_user_dependency, todo_id: int = Path(gt=0)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You have no rights to browse this resource")
    todo = db.scalar(select(Todo).where(Todo.id == todo_id))
    if not todo:
        raise HTTPException(status_code=404, detail="There is no such Todo")
    return todo


@router.put("/todos/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo_by_idt(todo: TodoUpdate, db: db_connection, current_user: current_user_dependency, todo_id: int = Path(gt=0)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You have no rights to browse this resource")
    todo_db: Todo = db.scalar(select(Todo).where(Todo.id == todo_id))
    if not todo_db:
        raise HTTPException(status_code=404, detail="There is no such Todo")
    todo_db.name = todo.name
    todo_db.description = todo.description
    todo_db.priority = todo.priority
    todo_db.is_done = todo.is_done

    db.add(todo_db)
    db.commit()


@router.delete('/todos/delete/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(db: db_connection, current_user: current_user_dependency, todo_id: int = Path(gt=0)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You have no rights to browse this resource")
    todo_db: Todo = db.scalar(select(Todo).where(Todo.id == todo_id))
    if not todo_db:
        raise HTTPException(status_code=404, detail="There is no such Todo")
    db.delete(todo_db)
    db.commit()

