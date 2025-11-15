from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_db_connection
from services.interfaces import TodoServiceInterface
from services.concrete import TodoService
from uow import SQLAUnitOfWork
from dao.concrete import SQLTodoDAO

from typing import Annotated
from fastapi import Depends
from services.interfaces import TodoServiceInterface


class DependencyService:
    @staticmethod
    def get_todo_service(
        db: AsyncSession = Depends(get_db_connection),
    ) -> TodoServiceInterface:
        uow = SQLAUnitOfWork(db)
        return TodoService(
            todo_dao=SQLTodoDAO(uow.db),
            uow=uow,
        )


todo_service = Annotated[
    TodoServiceInterface, Depends(DependencyService.get_todo_service)
]
