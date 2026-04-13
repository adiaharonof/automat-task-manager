from typing import List

from anyio.abc import TaskStatus

from Task import *
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.id_counter: int = 0


    def create_task(self, task: Task) -> Task:
        task.id = self.id_counter
        self.tasks[self.id_counter] = task
        self.id_counter += 1
        return task


    def delete_task(self, task_id: int) -> Task:
        if task_id not in self.tasks:
            raise ValueError(f'Task {task_id} does not exist')
        return self.tasks.pop(task_id)


    def get_all_tasks(self) -> List:
        return list(self.tasks.values())


    def get_completed_tasks(self) -> List:
        completed_tasks = []
        for task in self.tasks.values():
            if task.done:
                completed_tasks.append(task)
        return completed_tasks


    def get_uncompleted_tasks(self) -> List:
        uncompleted_tasks = []
        for task in self.tasks.values():
            if not task.done:
                uncompleted_tasks.append(task)
        return uncompleted_tasks


    def change_task_status(self, task_id: int, is_done: bool):
        task = self.get_task_by_id(task_id)
        task.change_task_status(is_done)
        return task


    def get_overdue_tasks(self) -> List:
        overdue_tasks = []
        for task in self.tasks.values():
            if not task.done and task.deadline is not None and task.deadline < datetime.now():
                overdue_tasks.append(task)
        return overdue_tasks


    def get_task_by_id(self, task_id: int) -> Task:
        if task_id not in self.tasks:
            raise ValueError(f'Task {task_id} does not exist')
        return self.tasks.get(task_id)
