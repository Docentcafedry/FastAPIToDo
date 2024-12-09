from fastapi import FastAPI
from database import Base, engine
from routes.auth import router as auth_router
from routes.todos import router as todo_router
from routes.admin import router as admin_router

Base.metadata.create_all(engine)


app = FastAPI()

app.include_router(auth_router)
app.include_router(todo_router)
app.include_router(admin_router)


