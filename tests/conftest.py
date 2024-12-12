import contextlib
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from depends.auth import get_current_user
from depends.db import db_connection
from main import app
from fastapi import Depends
from typing import Annotated
from models import Base
import random
import string


client = TestClient(app)

engine_test = create_engine("sqlite:///./test.db")

session_test = sessionmaker(bind=engine_test, autoflush=False, autocommit=False)


Base.metadata.create_all(bind=engine_test)


def get_random_string(length):
    # With combination of lower and upper case
    result_str = "".join(random.choice(string.ascii_letters) for i in range(length))
    # print random string


def get_db_connection_test():
    db = session_test()
    try:
        yield db
    finally:
        db.close()


def current_user_dep_replacement():
    return {"id": 1, "username": "user", "role": "admin", "is_active": True}


app.dependency_overrides[get_current_user] = current_user_dep_replacement
app.dependency_overrides[db_connection] = get_db_connection_test

@pytest.fixture
def session():
    session = session_test()
    yield session
    # Remove any data from database (even data not created by this session)
    session.rollback()  # rollback the transactions

    # truncate all tables
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(f'TRUNCATE {table.name} CASCADE;')
        session.commit()

    session.close()