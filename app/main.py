from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Literal

from .db import Base, engine, get_db
from .models import Todo

app = FastAPI(title="Todo Nimbus")

# 创建表
Base.metadata.create_all(bind=engine)

# 静态资源与模板
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, filter: Literal["all", "active", "completed"] = "all", db: Session = Depends(get_db)):
    q = db.query(Todo)
    if filter == "active":
        q = q.filter(Todo.completed.is_(False))
    elif filter == "completed":
        q = q.filter(Todo.completed.is_(True))
    todos = q.order_by(Todo.id.desc()).all()

    # 初始渲染整个页面
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos, "filter": filter})

@app.post("/add", response_class=HTMLResponse)
async def add_todo(title: str = Form(...), filter: str = Form("all"), db: Session = Depends(get_db)):
    title = title.strip()
    if title:
        todo = Todo(title=title)
        db.add(todo)
        db.commit()
    return _render_list_partial(db, filter)

@app.post("/toggle/{todo_id}", response_class=HTMLResponse)
async def toggle(todo_id: int, filter: str = Form("all"), db: Session = Depends(get_db)):
    todo = db.query(Todo).get(todo_id)
    if todo:
        todo.completed = not todo.completed
        db.commit()
    return _render_list_partial(db, filter)

@app.post("/delete/{todo_id}", response_class=HTMLResponse)
async def delete(todo_id: int, filter: str = Form("all"), db: Session = Depends(get_db)):
    todo = db.query(Todo).get(todo_id)
    if todo:
        db.delete(todo)
        db.commit()
    return _render_list_partial(db, filter)

# 工具函数：返回局部片段以供 HTMX 替换
from fastapi import BackgroundTasks

def _render_list_partial(db: Session, filter: str):
    q = db.query(Todo)
    if filter == "active":
        q = q.filter(Todo.completed.is_(False))
    elif filter == "completed":
        q = q.filter(Todo.completed.is_(True))
    todos = q.order_by(Todo.id.desc()).all()

    from fastapi import Request
    # 用一个伪 Request 来渲染片段（HTMX 只需要局部模板）
    class _FakeReq(Request):
        def __init__(self):
            scope = {"type": "http", "headers": []}
            super().__init__(scope)
    request = _FakeReq()
    return templates.TemplateResponse("_todo_list.html", {"request": request, "todos": todos, "filter": filter})