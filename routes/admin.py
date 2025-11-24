from fastapi import APIRouter, HTTPException, Path
from starlette import status
from depends.auth import current_user_dependency
from schemas import TodoUpdate
from services.dependency import todo_admin_service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_todos(current_user: current_user_dependency, service: todo_admin_service):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="You have no rights to browse this resource"
        )
    todos = await service.get_all_todos(user_id=current_user["id"])
    return todos


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(
    current_user: current_user_dependency,
    service: todo_admin_service,
    todo_id: int = Path(gt=0),
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403, detail="You have no rights to browse this resource"
        )
    todo = await service.get_by_id(todo_id=todo_id)
    return todo


@router.put("/todos/update/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo_by_idt(
    todo: TodoUpdate,
    service: todo_admin_service,
    current_user: current_user_dependency,
    todo_id: int = Path(gt=0),
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403, detail="You have no rights to browse this resource"
        )
    updated_todo = await service.update_todo(todo_id=todo_id, data=todo)
    return updated_todo


@router.delete("/todos/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(
    current_user: current_user_dependency,
    service: todo_admin_service,
    todo_id: int = Path(gt=0),
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403, detail="You have no rights to browse this resource"
        )
    await service.delete_todo(todo_id=todo_id)
