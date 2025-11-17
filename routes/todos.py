from fastapi import APIRouter, Path, HTTPException, Request
from starlette.responses import HTMLResponse, RedirectResponse
from depends.auth import get_current_user_from_token, current_user_cookie_dependency
from depends.db import db_connection
from starlette import status
from models import Todo
from sqlalchemy import select
from schemas import TodoCreate, TodoUpdate, Todo
from depends.auth import current_user_dependency
from fastapi.templating import Jinja2Templates
from services.dependency import todo_service
from utils import redirect_to_login


router = APIRouter(prefix="/todos", tags=["todos"])

templates = Jinja2Templates(directory="templates")


@router.get("/change/{todo_id}", response_class=HTMLResponse)
async def change_todo_page(
    request: Request,
    service: todo_service,
    current_user: current_user_cookie_dependency,
    todo_id: int = Path(gt=0),
):
    todo = await service.get_by_id_and_user(todo_id=todo_id, user_id=current_user["id"])

    return templates.TemplateResponse(
        request=request,
        name="change_todo.html",
        context={"title": "Update Todo", "todo": todo, "logout": True},
    )


@router.get("/todos/create", response_class=HTMLResponse)
async def todos_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="add_todo.html",
        context={"title": "Create Todo", "logout": True},
    )


@router.get("/todos", response_class=HTMLResponse)
async def todos_page(
    request: Request,
    service: todo_service,
    current_user: current_user_cookie_dependency,
):
    if not current_user:
        return redirect_to_login()

    todos = await service.get_all_todos_for_user(user_id=current_user["id"])
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={"title": "Todos", "todos": todos, "logout": True},
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_todos(db: db_connection, current_user: current_user_dependency):
    todos = db.scalars(
        select(Todo).filter(Todo.owner_id == current_user["id"]).order_by(Todo.id)
    ).all()
    return todos


@router.post("/create")
async def create_todo(
    todo: TodoCreate,
    service: todo_service,
    db: db_connection,
    current_user: current_user_dependency,
):
    new_todo = await service.create_todo(user_id=current_user["id"], data=todo)
    return new_todo


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(
    service: todo_service,
    todo_id: int = Path(gt=0),
):
    todo = await service.get_by_id_todo(todo_id=todo_id)
    return todo


@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo_by_idt(
    todo: TodoUpdate,
    db: db_connection,
    service: todo_service,
    current_user: current_user_dependency,
    todo_id: int = Path(gt=0),
):

    updated_todo = await service.update_todo(todo_id=todo_id, data=todo)
    return updated_todo


@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(
    service: todo_service,
    current_user: current_user_dependency,
    todo_id: int = Path(gt=0),
):
    await service.delete_todo(todo_id=todo_id)
