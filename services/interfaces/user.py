from abc import ABC, abstractmethod
from schemas import User, UserPasswordChange, UserCreate, UserUpdate
from typing import List, Optional


class UserServiceInterface(ABC):
    @abstractmethod
    async def create(self, data: UserCreate) -> User:
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:

        pass

    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def update(self, user_id: int, data: UserUpdate) -> User:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def change_password(self, user_id: int, data: UserPasswordChange) -> User:
        pass
