from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from routes.auth import router as auth_router
from routes.todos import router as todo_router
from routes.admin import router as admin_router
from routes.users import router as users_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(request=request, name='main.html', context={"title": "Todos"})



app.include_router(users_router)
app.include_router(auth_router)
app.include_router(todo_router)
app.include_router(admin_router)


