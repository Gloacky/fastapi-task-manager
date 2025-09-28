from pydantic import BaseModel
from typing import Optional
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    

class TaskCreate(TaskBase):
    completed: bool = False

class Task(TaskBase):
    id: int
    completed: bool

    class config:
        orm_mode = True