from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from datetime import datetime
from typing import List
from internal.dependencies import get_task_service
from internal.middlewares.auth import get_current_user_id
from internal.exceptions import InvalidTaskInput, DatabaseError
from internal.models.task import TaskService

class CreateTaskRequest(BaseModel):
    title: str
    description: str

class SingleTaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime

class ListTaskResponse(BaseModel):
    tasks: List[SingleTaskResponse]

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
                                  response_model=SingleTaskResponse, 
                                  status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("", 
                                  self.list, 
                                  methods=["GET"], 
                                  response_model=ListTaskResponse, 
                                  status_code=status.HTTP_200_OK)
        
    def create(self, 
               task: CreateTaskRequest, 
               current_user_id: str = Depends(get_current_user_id),
               task_service: TaskService = Depends(get_task_service)
        ):
        try:
            created_task = task_service.create(current_user_id, task.title, task.description)
        except InvalidTaskInput:
            raise HTTPException(status_code=400, detail="Invalid task title or description.")
        except DatabaseError as e:
            print(e)
            raise HTTPException(status_code=500, detail="Operation failed in database. Try again.")
        else:
            return SingleTaskResponse(
                id=created_task.id,
                user_id=created_task.user_id,
                title=created_task.title,
                description=created_task.description,
                is_completed=created_task.is_completed,
                created_at=created_task.created_at,
                updated_at=created_task.updated_at,
            )

    def list(self, 
            current_user_id: str = Depends(get_current_user_id),
            task_service: TaskService = Depends(get_task_service)):
        try:
            tasks = task_service.list(current_user_id)
        except DatabaseError as e:
            print(e)
            raise HTTPException(status_code=500, detail="Operation failed in database. Try again.")
        else:
            response_tasks: List[SingleTaskResponse] = []
            for t in tasks:
                response_tasks.append(SingleTaskResponse(
                    id=t.id,
                    user_id=t.user_id,
                    title=t.title,
                    description=t.description,
                    is_completed=t.is_completed,
                    created_at=t.created_at,
                    updated_at=t.updated_at,
                ))
            return ListTaskResponse(tasks=response_tasks)

task_controller = TaskController()