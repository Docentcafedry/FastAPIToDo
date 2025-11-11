from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from routes.auth import router as auth_router
from routes.todos import router as todo_router
from routes.admin import router as admin_router
from routes.users import router as users_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return RedirectResponse("/todos/todos", status_code=status.HTTP_302_FOUND)
    # return "application"



app.include_router(users_router)
app.include_router(auth_router)
app.include_router(todo_router)
app.include_router(admin_router)


