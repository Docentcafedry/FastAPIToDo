from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class ChangeUserNumber(BaseModel):
    number: str


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str
    role: str
    is_active: bool = Field(default=True)
    number: Optional[str] = None


class UserPasswordChange(BaseModel):
    new_password: str
    confirm_new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TodoCreate(BaseModel):
    name: str = Field(min_length=4, max_length=15, description="Todo name")
    description: str = Field(
        min_length=5, max_length=50, description="Todo description"
    )
    priority: int = Field(gt=0, lt=6, description="Todo priority")
    is_done: bool = Field(default=False, description="is done")


class TodoUpdate(TodoCreate):
    pass


class Todo(TodoCreate):
    id: str = Field(..., description="Todo ID")
