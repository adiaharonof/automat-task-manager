from fastapi import FastAPI, HTTPException
from Task import *
from TaskManager import *
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
TASK_MANAGER = TaskManager()

# allows all addresses to communicate with my API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# pydentic class that defines what the user needs to fill when creating a task,
# helps FastApi to convert and validate information received from the FrontEnd from JSON to a python object
class TaskCreate(BaseModel):
    task_title: str
    task_description: str
    task_deadline: Optional[datetime] = None


@app.post("/tasks")
def create_task(task_data: TaskCreate) -> Task:
    """
    receives all the needed information from the frontend after pydentic and creating a task using the Task and TaskManager classes.
    """
    try:
        new_task = Task(title=task_data.task_title, description=task_data.task_description,
                        deadline=task_data.task_deadline)
        TASK_MANAGER.create_task(new_task)
        return new_task
    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/tasks")
def get_tasks() -> List[Task]:
    return TASK_MANAGER.get_all_tasks()


@app.get("/tasks/completed")
def get_completed_tasks() -> List[Task]:
    return TASK_MANAGER.get_completed_tasks()


@app.get("/tasks/uncompleted")
def get_uncompleted_tasks() -> List[Task]:
    return TASK_MANAGER.get_uncompleted_tasks()


@app.get("/tasks/overdue")
def get_overdue_tasks() -> List[Task]:
    return TASK_MANAGER.get_overdue_tasks()


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> Task:
    """
    trying to delete a task and catching an error if the task doesn't exist.
    :param task_id:
    :return: the task itself
    """
    try:
        task = TASK_MANAGER.delete_task(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return task


@app.patch("/tasks/{task_id}")
def change_task_status(task_id: int, is_done: bool) -> Task:
    """changes the task status to Done / In progress"""
    try:
        return TASK_MANAGER.change_task_status(task_id, is_done)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.patch("/tasks/{task_id}/title")
def change_task_title(task_id: int, new_title: str) -> Task:
    try:
        edited_task = TASK_MANAGER.edit_task_title(task_id, new_title)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return edited_task


@app.patch("/tasks/{task_id}/description")
def change_task_description(task_id: int, new_description: str) -> Task:
    try:
        edited_task = TASK_MANAGER.edit_task_description(task_id, new_description)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return edited_task


if __name__ == '__main__':
    # using 0.0.0.0 and not Localhost in order to enable my docker to communicate
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
