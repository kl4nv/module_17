from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import app.schemas
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models.user import User
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(session: Annotated[Session, Depends(get_db)]):
    result = session.execute(select(User))
    return list(result.scalars().all())


@router.get('/user_id')
async def user_by_id(user_id: int,
                     session: Annotated[Session, Depends(get_db)]):
    select_user = session.execute(select(User).filter(User.id == user_id))
    select_user = select_user.scalar_one_or_none()

    if select_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    return select_user


@router.post('/creat')
async def create_user(createuser: CreateUser,
                      session: Annotated[Session, Depends(get_db)]):

    select_user = session.execute(select(User).filter(User.username == createuser.username))
    select_user = select_user.scalar_one_or_none()
    if select_user is not None:
        raise HTTPException(status_code=400, detail='user with this username exists')

    db_user = User(
            username=createuser.username,
            firstname=createuser.firstname,
            lastname=createuser.lastname,
            age=createuser.age,
            slug=slugify(createuser.username)
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_user(updateuser: UpdateUser,
                      user_id: int,
                      session: Annotated[Session, Depends(get_db)]):
    select_user = session.execute(select(User).filter(User.id == user_id))
    select_user = select_user.scalar_one_or_none()

    if select_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    session.execute(
        update(User)
        .where(User.id == user_id)
        .values(username=updateuser.username,
                firstname=updateuser.firstname,
                lastname=updateuser.lastname,
                age=updateuser.age,
                slug=slugify(updateuser.username),
                exclude_unset=True)
    )
    session.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete('/delete')
async def delete_user(
        user_id: int,
        session: Annotated[Session, Depends(get_db)]):
    select_user = session.execute(select(User).filter(User.id == user_id))
    select_user = select_user.scalar_one_or_none()

    if select_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    session.execute(delete(User).where(User.id == user_id))
    session.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}
