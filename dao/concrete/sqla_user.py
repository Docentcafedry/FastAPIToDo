from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from dao.interfaces import UserDAOInterface
from models import User as UserModel
from schemas import User, UserPasswordChange, UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SQLUserDAO(UserDAOInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError(f"User {user_id} not found")
        return User.model_validate(
            {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "is_active": user.is_active,
                "number": user.number,
            }
        )

    async def get_all_users(self) -> List[User]:
        result = await self.session.execute(select(UserModel))
        users = result.scalars().all()
        return [
            User.model_validate(
                {
                    "id": str(user.id),
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "is_active": user.is_active,
                    "number": user.number,
                }
            )
            for user in users
        ]

    async def create_user(
        self,
        data: UserCreate,
    ) -> User:
        print("enter")
        user: UserModel = UserModel(**data.model_dump())
        self.session.add(user)
        await self.session.flush()
        print(user)

        schema = User.model_validate(
            {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "is_active": user.is_active,
                "number": user.number,
            }
        )

        return schema

    async def update_user(self, user_id: int, data: UserUpdate) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_db = result.scalar_one_or_none()
        if not user_db:
            raise ValueError(f"Todo {user_id} not found")

        for k, v in data.model_dump():
            setattr(user_db, k, v)

        await self.session.flush()

        return await self.get_user_by_id(user_db.id)

    async def delete(self, user_id: int) -> None:
        await self.session.execute(delete(UserModel).where(UserModel.id == user_id))

        await self.session.flush()

    async def change_user_password(
        self, user_id: int, data: UserPasswordChange
    ) -> User:
        user = await self.get_user_by_id(user_id=user_id)
        hashed_password = pwd_context.hash(data.new_password)
        user.hashed_password = hashed_password
        self.session.add(user)
        await self.session.commit()
        return user

    async def delete_user(self, user_id: int) -> None:
        await self.session.execute(delete(UserModel).where(UserModel.id == user_id))
        await self.session.flush()
