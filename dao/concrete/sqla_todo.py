from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from dao.interfaces import TodoDAOInterface
from models import Todo as TodoModel
from schemas import TodoCreate, TodoUpdate, Todo


class SQLTodoDAO(TodoDAOInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, todo_id: int) -> Optional[Todo]:
        result = await self.session.execute(
            select(TodoModel).where(TodoModel.id == todo_id)
        )
        todo = result.scalar_one_or_none()
        if not todo:
            return None
        return Todo.model_validate(todo)

    async def get_all(self) -> List[Todo]:
        result = await self.session.execute(select(TodoModel))
        todos = result.scalars().all()
        return [
            Todo.model_validate(
                {
                    "id": str(todo.id),
                    "name": todo.name,
                    "description": todo.description,
                    "is_done": todo.is_done,
                    "priority": todo.priority,
                    "owner_id": todo.owner_id,
                }
            )
            for todo in todos
        ]

    async def create(
        self,
        user_id: int,
        data: TodoCreate,
    ) -> Todo:
        todo = TodoModel(
            name=data.name,
            description=data.description,
            is_done=data.is_done,
            priority=data.priority,
            owner_id=user_id,
        )
        self.session.add(todo)
        await self.session.flush()

        schema = Todo(
            id=str(todo.id),
            name=todo.name,
            description=todo.description,
            priority=todo.priority,
            is_done=todo.is_done,
            owner_id=user_id,
        )
        print(schema)

        return schema

    async def update(self, todo_id: int, data: TodoUpdate) -> Optional:
        result = await self.session.execute(
            select(TodoModel).where(TodoModel.id == todo_id)
        )
        todo_db = await result.scalar_one_or_none()
        if not todo_db:
            raise ValueError(f"Todo {todo_id} not found")
        todo_db.name = data.name
        todo_db.description = data.description
        todo_db.priority = data.priority
        todo_db.is_done = data.is_done

        await self.session.flush()

        return await self.get_by_id(todo_id)

    async def delete(self, todo_id: int) -> None:
        await self.session.execute(delete(TodoModel).where(TodoModel.id == todo_id))

        await self.session.flush()
