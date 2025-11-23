from abc import ABC, abstractmethod
from schemas import Todo, TodoCreate, TodoUpdate
from typing import List, Optional


class TodoServiceInterface(ABC):
    @abstractmethod
    async def create_todo(self, user_id: int, data: TodoCreate) -> Todo:
        pass

    @abstractmethod
    async def get_all_todos(self, user_id: Optional[int]) -> List[Todo]:

        pass

    @abstractmethod
    async def get_by_id(self, todo_id: int, user_id: Optional[int]) -> Optional[Todo]:
        pass

    @abstractmethod
    async def update_todo(
        self, todo_id: int, data: TodoUpdate, user_id: Optional[int]
    ) -> Todo:
        pass

    @abstractmethod
    async def delete_todo(self, todo_id: int, user_id: Optional[int]) -> None:
        pass
