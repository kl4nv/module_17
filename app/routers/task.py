from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import app.schemas
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models.task import Task
from app.schemas import CreateTask, UpdateTask
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])

@router.get('/')
async def all_tasks(session: Annotated[Session, Depends(get_db)]):
    result = session.execute(select(Task))
    return list(result.scalars().all())

@router.get('/task_id')
async def task_by_id(task_id: int,
                     session: Annotated[Session, Depends(get_db)]):
    select_Task = session.execute(select(Task).filter(Task.id == task_id))
    select_Task = select_Task.scalar_one_or_none()

    if select_Task is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    return select_Task

@router.post('/creat')
async def create_task(createTask: CreateTask,
                      user_id: int,
                      session: Annotated[Session, Depends(get_db)]):

    select_Task = session.execute(select(Task).filter(Task.title == createTask.title))
    select_Task = select_Task.scalar_one_or_none()
    if select_Task is not None:
        raise HTTPException(status_code=400, detail='Task with this title exists')

    db_Task = Task(
            title=createTask.title,
            content=createTask.content,
            priority=createTask.priority,
            completed=False,
            slug=slugify(createTask.title),
            user_id=user_id
    )

    session.add(db_Task)
    session.commit()
    session.refresh(db_Task)
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put('/update')
async def update_task(updateTask: UpdateTask,
                      Task_id: int,
                      session: Annotated[Session, Depends(get_db)]):
    select_Task = session.execute(select(Task).filter(Task.id == Task_id))
    select_Task = select_Task.scalar_one_or_none()

    if select_Task is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    session.execute(
        update(Task)
        .where(Task.id == Task_id)
        .values(
            id=updateTask.id,
            title=updateTask.title,
            content=updateTask.priority,
            priority=updateTask.priority,
            completed=updateTask.completed,
            slug=slugify(updateTask.slug),
            user=updateTask.user,
            exclude_unset=True)
    )
    session.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}

@router.delete('/delete')
async def delete_task(
        Task_id: int,
        session: Annotated[Session, Depends(get_db)]):
    select_Task = session.execute(select(Task).filter(Task.id == Task_id))
    select_Task = select_Task.scalar_one_or_none()

    if select_Task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    session.execute(delete(Task).where(Task.id == Task_id))
    session.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'}
