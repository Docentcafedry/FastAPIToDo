from fastapi import APIRouter, Path, HTTPException
from depends.db import db_connection
from starlette import status
from models import Todo
from sqlalchemy import select
from schemas import ChangeUserNumber
from depends.auth import current_user_dependency
from models import User
from services.dependency import user_service


router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/change-number", status_code=status.HTTP_204_NO_CONTENT)
async def get_todos(
    current_user: current_user_dependency, data: ChangeUserNumber, service: user_service
):
    await service.update(user_id=current_user["id"], data=data)
