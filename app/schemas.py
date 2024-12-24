from pydantic import BaseModel, Field
from typing import Annotated

class CreateUser(BaseModel):
    username: Annotated[str, Field()]
    firstname: Annotated[str, Field()]
    lastname: Annotated[str, Field()]
    age: Annotated[int, Field()]


class UpdateUser(BaseModel):
    firstname: Annotated[str, Field()]
    lastname: Annotated[str, Field()]
    age: Annotated[int, Field()]


class CreateTask(BaseModel):
    title: Annotated[str, Field()]
    content: Annotated[str, Field()]
    priority: Annotated[str, Field()]


class UpdateTask(BaseModel):
    title: Annotated[str, Field()]
    content: Annotated[str, Field()]
    priority: Annotated[str, Field()]
