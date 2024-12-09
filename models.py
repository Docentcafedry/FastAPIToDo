from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Integer, ForeignKey


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    first_name: Mapped[str] = mapped_column(String(15))
    last_name: Mapped[str] = mapped_column(String(15))
    hashed_password: Mapped[str] = mapped_column(String())
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str] = mapped_column(String())


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(50))
    priority: Mapped[int] = mapped_column()
    is_done: Mapped[bool] = mapped_column(Boolean(), default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
