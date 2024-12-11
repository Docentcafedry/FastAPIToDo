from fastapi import APIRouter, Path, HTTPException
from depends.db import db_connection
from starlette import status
from models import Todo
from sqlalchemy import select
from schemas import ChangeUserNumber
from depends.auth import current_user_dependency
from models import User


router = APIRouter(prefix='/users', tags=['users'])


@router.patch("/change-number", status_code=status.HTTP_204_NO_CONTENT)
async def get_todos(db: db_connection, current_user: current_user_dependency, data: ChangeUserNumber):
    user: User = db.scalar(select(User).filter(User.id == current_user.id))
    user.number = data.number
    db.add(user)
    db.commit()
