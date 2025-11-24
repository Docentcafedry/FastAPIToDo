from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db_connection
from services.concrete import TodoService, UserService, TodoAdminService
from uow import SQLAUnitOfWork
from dao.concrete import SQLTodoDAO, SQLTodoAdminDAO, SQLUserDAO
from typing import Annotated
from fastapi import Depends
from services.interfaces import TodoServiceInterface, UserServiceInterface


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

    @staticmethod
    def get_user_service(
        db: AsyncSession = Depends(get_db_connection),
    ) -> UserServiceInterface:
        uow = SQLAUnitOfWork(db)
        return UserService(user_dao=SQLUserDAO(uow.db), uow=uow)

    @staticmethod
    def get_todo_admin_service(
        db: AsyncSession = Depends(get_db_connection),
    ) -> TodoServiceInterface:
        uow = SQLAUnitOfWork(db)
        return TodoAdminService(todo_dao=SQLTodoAdminDAO(uow.db), uow=uow)


todo_service = Annotated[
    TodoServiceInterface, Depends(DependencyService.get_todo_service)
]

user_service = Annotated[
    UserServiceInterface, Depends(DependencyService.get_user_service)
]

todo_admin_service = Annotated[
    TodoServiceInterface, Depends(DependencyService.get_todo_admin_service)
]
