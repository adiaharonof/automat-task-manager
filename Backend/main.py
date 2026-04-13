from fastapi import FastAPI, HTTPException
from Task import *
from TaskManager import *
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
TASK_MANAGER = TaskManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskCreate(BaseModel):
    task_title: str
    task_description: str
    task_deadline: Optional[datetime] = None

@app.post("/tasks")
def create_task(task_data: TaskCreate) -> Task:
    try:
        new_task = Task(title=task_data.task_title, description=task_data.task_description, deadline=task_data.task_deadline)
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
    try:
        task = TASK_MANAGER.delete_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return task


@app.patch("/tasks/{task_id}")
def change_task_status(task_id: int, is_done:bool) -> Task:
    try:
        return TASK_MANAGER.change_task_status(task_id, is_done)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == '__main__':
    #using 0.0.0.0 and not Localhost in order to enable my docker to communicate
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

