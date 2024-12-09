from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str
    role: str
    is_active: bool = Field(default=True)


class UserPasswordChange(BaseModel):
    new_password: str
    confirm_new_password: str



class Token(BaseModel):
    access_token: str
    token_type: str

class TodoCreate(BaseModel):
    name: str = Field(min_length=4, max_length=15)
    description: str = Field(min_length=5, max_length=50)
    priority: int = Field(gt=0, lt=6)
    is_done: bool = Field(default=False)

class TodoUpdate(TodoCreate):
    pass
