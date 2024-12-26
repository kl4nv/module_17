from fastapi import FastAPI
from app.models.user import User  # Импортируем User
from app.models.task import Task
from app.routers import task, user

app = FastAPI()


@app.get('/')
async def welcome_message():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)