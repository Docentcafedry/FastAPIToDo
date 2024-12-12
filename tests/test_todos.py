from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from depends.auth import current_user_dependency
from depends.db import db_connection
from main import app
from fastapi import Depends
from typing import Annotated
from schemas import UserCreate

client = TestClient(app)

engine_test = create_engine("sqlite:///./test.db")

session_test = sessionmaker(bind=engine_test, autoflush=False, autocommit=False)


def get_db_connection_test():
    db = session_test()
    try:
        yield db
    finally:
        db.close()


def current_user_dep_replacement():
    return {"id": 1, "username": "user", "role": "admin"}


current_user_dependency_test = Annotated[dict, Depends(current_user_dep_replacement)]

app.dependency_overrides[current_user_dependency] = current_user_dependency_test
app.dependency_overrides[db_connection] = get_db_connection_test


def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {}


