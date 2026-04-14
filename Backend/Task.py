from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, model_validator

def utc_now():
    return datetime.now(timezone.utc)

class Task(BaseModel):
    title: str
    description: str
    deadline: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    id: int = None
    done: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    def change_task_status(self, status: bool):
        """Change the status of the task to Done/ not Done and updates the completed at time."""
        if self.done is False and status is True:
            self.completed_at = datetime.now(timezone.utc)
        self.done = status
        return self

    @model_validator(mode='after')
    def _validates(self):
        """ validates when creating a new task that it's title or description isn't too long
         and that the deadline date has not passed yet."""
        if self.deadline is not None and self.created_at > self.deadline:
            raise ValueError("the date of the deadline is in the past")
        if len(self.description) > 70:
            raise ValueError("Task description too long, must be under 70 characters")
        if len(self.title) > 50:
            raise ValueError("title must be under 50 characters")
        return self

    def edit_title(self, new_title: str):
        """gets a new title, checks it is not too long or empty and Changes the title of the task"""
        if len(new_title) == 0 or len(new_title) > 50:
            raise ValueError("Title can not be null or above 50 characters")
        self.title = new_title
        return self


    def edit_description(self, new_description: str):
        """gets a new description, checks it is not too long and Changes the description of the task"""
        if len(new_description) == 0 or len(new_description) > 70:
            raise ValueError("description can not be null or above 70 characters")
        self.description = new_description
        return self

