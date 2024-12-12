import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from models import User
from depends.db import db_connection
from passlib.context import CryptContext
from sqlalchemy import select
from dotenv import load_dotenv
from schemas import Token
from datetime import timedelta
from features.jwt_features import create_access_token
from starlette import status
from schemas import UserCreate, UserPasswordChange
from depends.auth import current_user_dependency

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix='/auth', tags=["auth"])


@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def sign_up(db: db_connection, user_data: UserCreate):
    hashed_password = pwd_context.hash(user_data.password)
    user: User = User(email=user_data.email, username=user_data.username, first_name=user_data.first_name, last_name=user_data.last_name, hashed_password=hashed_password, role=user_data.role)
    db.add(user)
    db.commit()
    return user


@router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def auth_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: db_connection):
    user = db.scalar(select(User).where(User.username == form_data.username))
    if not user:
        raise HTTPException(status_code=401, detail="Bad credentials")
    passwords_match = pwd_context.verify(form_data.password, user.hashed_password)
    if not passwords_match:
        raise HTTPException(status_code=401, detail="Bad credentials")

    payload = {'username': user.username, 'id': user.id, "role": user.role}

    access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
        data=payload, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me", status_code=status.HTTP_200_OK)
async def get_current_user(current_user: current_user_dependency):
    return current_user


@router.patch("/users/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_current_password(db: db_connection, current_user: current_user_dependency, form_data: UserPasswordChange):
    if not form_data.new_password == form_data.confirm_new_password:
        raise HTTPException(status_code=400, detail="Passwords should match")
    user = user = db.scalar(select(User).where(User.username == current_user["username"]))
    hashed_password = pwd_context.hash(form_data.new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()

