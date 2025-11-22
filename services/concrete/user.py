import os

from fastapi.security import OAuth2PasswordRequestForm

from features.jwt_features import create_access_token
from schemas import User, UserPasswordChange, UserCreate, UserUpdate
from typing import List, Optional
from services.interfaces import UserServiceInterface
from dao.concrete import SQLUserDAO
from uow import BaseUnitOfWork
from passlib.context import CryptContext
from fastapi import HTTPException
from datetime import timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(UserServiceInterface):

    def __init__(self, user_dao: SQLUserDAO, uow: BaseUnitOfWork):
        self.user_dao = user_dao
        self.uow = uow

    async def create(self, data: UserCreate) -> User:
        data.hashed_password = pwd_context.hash(data.password)
        delattr(data, "password")
        async with self.uow:
            user = await self.user_dao.create_user(data=data)
            return user

    async def get_all(self) -> List[User]:
        async with self.uow:
            users = await self.user_dao.get_all_users()
            return users

    async def get_user(self, user_id: int) -> Optional[User]:
        async with self.uow:
            user = await self.user_dao.get_user_by_id(user_id=user_id)
            return user

    async def update(self, user_id: int, data: UserUpdate) -> User:
        async with self.uow:
            updated_user = await self.user_dao.update_user(user_id=user_id, data=data)
            return updated_user

    async def delete(self, user_id: int) -> None:
        async with self.uow:
            await self.user_dao.delete(user_id=user_id)

    async def change_password(self, user_id: int, data: UserPasswordChange) -> User:
        if not data.new_password == data.confirm_new_password:
            raise ValueError("Passwords should match")
        async with self.uow:
            user = await self.user_dao.change_user_password(user_id=user_id, data=data)
            return user

    async def validate_user(self, data: OAuth2PasswordRequestForm) -> Optional[str]:
        user = await self.user_dao.get_user_by_username(username=data.username)
        passwords_match = pwd_context.verify(data.password, user.password)
        if not passwords_match:
            raise HTTPException(status_code=401, detail="Bad credentials")

        payload = {"username": user.username, "id": user.id, "role": user.role}

        access_token_expires = timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
        access_token = create_access_token(
            data=payload, expires_delta=access_token_expires
        )
        return access_token
