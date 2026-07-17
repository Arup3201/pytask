from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Protocol
from datetime import datetime
from internal.dependencies import get_task_service
from internal.middlewares.auth import get_current_user_id
from internal.dataclasses import TaskData
from internal.exceptions import InvalidTaskInput, DatabaseError

class TaskServiceProtocol(Protocol):
    def create(self, user_id: str, title: str, description: str) -> TaskData:
        ...


class CreateTaskRequest(BaseModel):
    title: str
    description: str

class CreateTaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime

class TaskController:
    def __init__(self):
        self.router = APIRouter(
            prefix="/tasks",
            tags=["tasks"]
        )
        self.__register_routes()

    def __register_routes(self):
        self.router.add_api_route("", 
                                  self.create, 
                                  methods=["POST"], 
                                  response_model=CreateTaskResponse, 
                                  status_code=status.HTTP_201_CREATED)
        
    def create(self, 
               task: CreateTaskRequest, 
               current_user_id: str = Depends(get_current_user_id),
               task_service: TaskServiceProtocol = Depends(get_task_service)
        ):
        try:
            created_task = task_service.create(current_user_id, task.title, task.description)
        except InvalidTaskInput:
            raise HTTPException(status_code=400, detail="Invalid task title or description.")
        except DatabaseError as e:
            print(e)
            raise HTTPException(status_code=500, detail="Operation failed in database. Try again.")
        else:
            return CreateTaskResponse(
                id=created_task.id,
                user_id=created_task.user_id,
                title=created_task.title,
                description=created_task.description,
                is_completed=created_task.is_completed,
                created_at=created_task.created_at,
                updated_at=created_task.updated_at,
            )

task_controller = TaskController()