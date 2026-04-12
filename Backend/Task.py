from datetime import datetime

class Task:
    def __init__(self, title: str, description: str, deadline: datetime = None, id: int = None, done: bool = False, completed_at: datetime = None):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.completed_at = completed_at
        self.deadline = deadline
        self.created_at = datetime.now()
        self._validates()


    def change_task_status(self, status: bool):
        if self.done is False and status is True:
            self.completed_at = datetime.now()
        self.done = status
        return self

    def _validates(self):
        if self.deadline is not None and self.created_at > self.deadline:
            raise ValueError("the date of the deadline is in the past")
        if self.completed_at is not None and not isinstance(self.completed_at, datetime):
            raise TypeError("Task completion date must be of type datetime")
        if self.deadline is not None and not isinstance(self.deadline, datetime):
            raise TypeError("Task deadline must be of type datetime")
        if not isinstance(self.done, bool):
            raise TypeError("done must be a boolean")
        if not isinstance(self.title, str):
            raise TypeError("title must be a string")
        if not isinstance(self.description, str):
            raise TypeError("description must be a string")
        if len(self.description) > 70:
            raise ValueError("Task description too long, must be under 70 characters")
        if len(self.title) > 50:
            raise ValueError("title must be under 50 characters")




