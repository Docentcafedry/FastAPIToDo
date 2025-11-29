import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import get_db_connection
from depends.auth import get_current_user, get_current_active_user
from depends.db import db_connection
from main import app
from fastapi import Depends
from typing import Annotated
from models import Base
import random
import string
from sqlalchemy import text
from models import Todo, User
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import asyncio
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import aiosqlite

client = TestClient(app)

engine_test = create_async_engine("sqlite+aiosqlite:///./test.db")

session_test = sessionmaker(
    engine_test,
    expire_on_commit=False,
    class_=AsyncSession,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_random_string(length):
    # With combination of lower and upper case
    result_str = "".join(random.choice(string.ascii_letters) for i in range(length))
    # print random string


async def get_db_connection_test():
    db = session_test()
    try:
        yield db
    finally:
        await db.close()


def current_user_dep_replacement():
    return {"id": 1, "username": "user", "role": "admin", "is_active": True}


# app.dependency_overrides[get_current_active_user] = current_user_dep_replacement
app.dependency_overrides[get_db_connection] = get_db_connection_test


@pytest_asyncio.fixture(scope="session", autouse=True)
async def fake_db():
    from models import Base

    db = session_test()
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield db
    finally:
        await db.close()


@pytest_asyncio.fixture(scope="function")
async def session():
    session = session_test()
    yield session
    # Remove any data from database (even data not created by this session)
    await session.rollback()  # rollback the transactions

    # truncate all tables
    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(text(f"DELETE FROM {table.name};"))
        await session.commit()

    await session.close()


@pytest_asyncio.fixture(scope="function")
async def create_user():
    hashed_password = pwd_context.hash("123456")
    user: User = User(
        email="user1@example.com",
        username="string1",
        first_name="string",
        last_name="string",
        hashed_password=hashed_password,
        role="admin",
    )
    db = session_test()
    print(db)
    db.add(user)
    await db.commit()


@pytest_asyncio.fixture(scope="function")
async def create_todo():
    todo: Todo = Todo(name="String", description="test todo", priority=2, owner_id=1)
    db = session_test()
    print(db)
    db.add(todo)
    await db.commit()
