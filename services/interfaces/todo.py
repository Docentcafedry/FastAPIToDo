from abc import ABC, abstractmethod
from schemas import Todo, TodoCreate, TodoUpdate
from typing import List, Optional


class TodoServiceInterface(ABC):
    @abstractmethod
    async def create_todo(self, user_id: int, data: TodoCreate) -> Todo:
        pass

    @abstractmethod
    async def get_all_todos(self) -> List[Todo]:

        pass

    @abstractmethod
    async def get_all_todos_for_user(self, user_id: int) -> List[Todo]:

        pass

    @abstractmethod
    async def get_by_id_and_user(self, todo_id: int, user_id: int) -> Optional[Todo]:
        pass

    @abstractmethod
    async def update_todo(self, todo_id: int, data: TodoUpdate) -> Todo:
        pass

    @abstractmethod
    async def delete_todo(self, todo_id: int) -> None:
        pass

    @abstractmethod
    async def delete_todo_by_owner(self, todo_id: int, user_id: int) -> None:
        pass

    @abstractmethod
    async def get_by_id_todo(self, todo_id: int) -> Optional[Todo]:

        pass
