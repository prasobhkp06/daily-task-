from typing import Optional
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    email: str
    password: str = Field(min_length=3)


class UserLogin(BaseModel):
    username: str
    password: str


class TaskCreate(BaseModel):
    username: str
    title: str = Field(min_length=1)
    description: str = ""
    priority: str = "Medium"
    due_date: Optional[str] = None
    category: str = "General"


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""
    priority: str = "Medium"
    due_date: Optional[str] = None
    completed: bool = False
    category: str = "General"


class TaskComplete(BaseModel):
    completed: bool = True
