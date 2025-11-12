from abc import ABC, abstractmethod
from typing import List, Optional

from schemas import Todo, TodoCreate, TodoUpdate


class TodoDAOInterface(ABC):  # pragma: no cover
    """Interface for beer data access."""

    @abstractmethod
    async def get_by_id(self, todo_id: str) -> Optional[Todo]:

        pass

    @abstractmethod
    async def get_all(self) -> List[Todo]:

        pass

    @abstractmethod
    async def create(self, user_id: int, data: TodoCreate) -> Todo:
        pass

    @abstractmethod
    async def update(self, todo_id: int, data: TodoUpdate) -> Todo:
        pass

    @abstractmethod
    async def delete(self, todo_id: int) -> None:
        pass
