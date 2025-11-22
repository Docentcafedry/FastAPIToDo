from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


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
    hashed_password: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[str] = None
    number: Optional[str] = None


class User(BaseModel):
    id: str = Field(description="Todo ID")
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role: str
    is_active: bool = Field(default=True)
    number: Optional[str] = None


class UserDB(User):
    password: str


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
    id: str = Field(description="Todo ID")
    owner_id: int = Field(description="Owner ID")


class ErrorResponse(BaseModel):
    code: str
    details: str
    message: Optional[str] = None
    key: Optional[str] = None


class ErrorEnvelope(BaseModel):
    errors: List[ErrorResponse]
