from fastapi import APIRouter, Path, HTTPException, Request
from starlette.responses import HTMLResponse, RedirectResponse
from depends.auth import get_current_user_from_token
from depends.db import db_connection
from starlette import status
from models import Todo
from sqlalchemy import select
from schemas import TodoCreate, TodoUpdate, Todo
from depends.auth import current_user_dependency
from fastapi.templating import Jinja2Templates
from services.dependency import todo_service


router = APIRouter(prefix="/todos", tags=["todos"])

templates = Jinja2Templates(directory="templates")


def redirect_to_login():
    redirect_response = RedirectResponse(
        url="/auth/login", status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


@router.get("/change/{todo_id}", response_class=HTMLResponse)
async def change_todo_page(
    request: Request,
    service: db_connection,
    db: db_connection,
    todo_id: int = Path(gt=0),
):
    try:
        access_token = request.cookies.get("access_token")
        user = await get_current_user_from_token(access_token, db)

        if not user:
            redirect_to_login()
        todo = db.scalar(
            select(Todo).where(Todo.id == todo_id).where(Todo.owner_id == user.id)
        )
        return templates.TemplateResponse(
            request=request,
            name="change_todo.html",
            context={"title": "Update Todo", "todo": todo, "logout": True},
        )
    except:
        redirect_to_login()
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
async def todos_page(request: Request, service: todo_service, db: db_connection):
    try:
        access_token = request.cookies.get("access_token")
        user = await get_current_user_from_token(access_token, db)

        if not user:
            redirect_to_login()
        todos = await service.get_all_todos()
        return templates.TemplateResponse(
            request=request,
            name="todo.html",
            context={"title": "Todos", "todos": todos, "logout": True},
        )
    except:
        redirect_to_login()
    # return templates.TemplateResponse(request=request, name='todo.html', context={"title": "Todos", "todos": todos})
    return "hello"


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
    db: db_connection, current_user: current_user_dependency, todo_id: int = Path(gt=0)
):
    todo = db.scalar(
        select(Todo)
        .where(Todo.id == todo_id)
        .where(Todo.owner_id == current_user["id"])
    )
    if not todo:
        raise HTTPException(status_code=404, detail="There is no such Todo")
    return todo


@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo_by_idt(
    todo: TodoUpdate,
    db: db_connection,
    current_user: current_user_dependency,
    todo_id: int = Path(gt=0),
):
    todo_db: Todo = db.scalar(select(Todo).where(Todo.id == todo_id))
    if not todo_db:
        raise HTTPException(status_code=404, detail="There is no such Todo")
    if todo_db.owner_id != current_user["id"]:
        raise HTTPException(403, detail="You have no rights to update this record")
    todo_db.name = todo.name
    todo_db.description = todo.description
    todo_db.priority = todo.priority
    todo_db.is_done = todo.is_done

    db.add(todo_db)
    db.commit()


@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(
    db: db_connection, current_user: current_user_dependency, todo_id: int = Path(gt=0)
):
    todo_db: Todo = db.scalar(select(Todo).where(Todo.id == todo_id))
    if not todo_db:
        raise HTTPException(status_code=404, detail="There is no such Todo")
    if todo_db.owner_id != current_user["id"]:
        raise HTTPException(403, detail="You have no rights to update this record")
    db.delete(todo_db)
    db.commit()
