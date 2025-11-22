from abc import ABC, abstractmethod
from typing import List, Optional

from schemas import UserCreate, UserPasswordChange, ChangeUserNumber, User, UserUpdate


class UserDAOInterface(ABC):  # pragma: no cover

    @abstractmethod
    async def create_user(self, data: UserCreate) -> Optional[User]:

        pass

    @abstractmethod
    async def update_user(self, user_id: int, data: UserUpdate) -> User:

        pass

    @abstractmethod
    async def get_all_users(self) -> List[User]:

        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:

        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:

        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def change_user_password(
        self, user_id: int, data: UserPasswordChange
    ) -> User:
        pass
