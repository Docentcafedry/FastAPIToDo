from fastapi import APIRouter, Path, HTTPException
from depends.db import db_connection
from starlette import status
from models import Todo
from sqlalchemy import select
from schemas import TodoCreate, TodoUpdate
from depends.auth import current_user_dependency


router = APIRouter(prefix='/todos', tags=['todos'])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_todos(db: db_connection, current_user: current_user_dependency):
    todos = db.scalars(select(Todo).filter(Todo.owner_id == current_user["id"]).order_by(Todo.id)).all()
    return todos


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, db: db_connection, current_user: current_user_dependency):
    new_todo: Todo = Todo(**todo.model_dump(), owner_id=current_user.id)
    db.add(new_todo)
    db.commit()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_connection, current_user: current_user_dependency, todo_id: int = Path(gt=0)):
    todo = db.scalar(select(Todo).where(Todo.id == todo_id).where(Todo.owner_id == current_user.id))
    if not todo:
        raise HTTPException(status_code=404, detail="There is no such Todo")
    return todo


@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo_by_idt(todo: TodoUpdate, db: db_connection, current_user: current_user_dependency, todo_id: int = Path(gt=0)):
    todo_db: Todo = db.scalar(select(Todo).where(Todo.id == todo_id))
    if not todo_db:
        raise HTTPException(status_code=404, detail="There is no such Todo")
    if todo_db.owner_id != current_user.id:
        raise HTTPException(403, detail="You have no rights to update this record")
    todo_db.name = todo.name
    todo_db.description = todo.description
    todo_db.priority = todo.priority
    todo_db.is_done = todo.is_done

    db.add(todo_db)
    db.commit()


@router.delete('/delete/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(db: db_connection, current_user: current_user_dependency, todo_id: int = Path(gt=0)):
    todo_db: Todo = db.scalar(select(Todo).where(Todo.id == todo_id))
    if not todo_db:
        raise HTTPException(status_code=404, detail="There is no such Todo")
    if todo_db.owner_id != current_user.id:
        raise HTTPException(403, detail="You have no rights to update this record")
    db.delete(todo_db)
    db.commit()
    