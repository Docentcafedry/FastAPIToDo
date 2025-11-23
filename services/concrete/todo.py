from dao.concrete import SQLTodoDAO, SQLTodoAdminDAO
from uow import BaseUnitOfWork
from services.interfaces import TodoServiceInterface
from schemas import Todo, TodoUpdate, TodoCreate
from typing import Optional, List
from exceptions import NotFoundError


class TodoService(TodoServiceInterface):
    def __init__(self, todo_dao: SQLTodoDAO, uow: BaseUnitOfWork):
        self.todo_dao = todo_dao
        self.uow = uow

    async def create_todo(self, user_id: int, data: TodoCreate) -> Todo:
        async with self.uow:
            todo = await self.todo_dao.create(user_id=user_id, data=data)
            return todo

    async def get_by_id(self, todo_id: int, user_id: int) -> Optional[Todo]:
        async with self.uow:
            todo = await self.todo_dao.get_by_id(todo_id=todo_id, user_id=user_id)

            if not todo:
                raise NotFoundError(resource_type="todo", resource_id=str(todo_id))
            return todo

    async def get_all_todos(self, user_id: int) -> List[Todo]:
        async with self.uow:
            todos = await self.todo_dao.get_all(user_id=user_id)
            return todos

    async def update_todo(self, todo_id: int, data: TodoUpdate, user_id: int) -> Todo:
        async with self.uow:
            updated_todo = await self.todo_dao.update(
                todo_id=todo_id, user_id=user_id, data=data
            )
            return updated_todo

    async def delete_todo(self, todo_id: int, user_id: int) -> None:
        async with self.uow:
            await self.todo_dao.delete(todo_id=todo_id, user_id=user_id)


class TodoAdminService(TodoServiceInterface):
    def __init__(self, todo_dao: SQLTodoAdminDAO, uow: BaseUnitOfWork):
        self.todo_dao = todo_dao
        self.uow = uow

    async def create_todo(self, user_id: int, data: TodoCreate) -> Todo:
        async with self.uow:
            todo = await self.todo_dao.create(user_id=user_id, data=data)
            return todo

    async def get_by_id(self, todo_id: int, user_id=None) -> Optional[Todo]:
        async with self.uow:
            todo = await self.todo_dao.get_by_id(todo_id=todo_id)

            if not todo:
                raise NotFoundError(resource_type="todo", resource_id=str(todo_id))
            return todo

    async def get_all_todos(self, user_id=None) -> List[Todo]:
        async with self.uow:
            todos = await self.todo_dao.get_all()
            return todos

    async def update_todo(self, todo_id: int, data: TodoUpdate, user_id=None) -> Todo:
        async with self.uow:
            updated_todo = await self.todo_dao.update(todo_id=todo_id, data=data)
            return updated_todo

    async def delete_todo(self, todo_id: int, user_id=None) -> None:
        async with self.uow:
            await self.todo_dao.delete(todo_id=todo_id)
