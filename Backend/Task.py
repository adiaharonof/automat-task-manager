from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class Task(BaseModel):
    title: str
    description: str
    deadline: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    id: int = None
    done: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    def change_task_status(self, status: bool):
        """Change the status of the task to Done/ not Done and updates the completed at time."""
        if self.done is False and status is True:
            self.completed_at = datetime.now()
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
