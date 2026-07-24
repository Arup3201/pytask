import uuid
from typing import List
from internal.dataclasses import TaskData
from internal.exceptions import InvalidTaskInput, IlligalUpdate, DatabaseError
from internal.stores.task import TaskStore

class TaskService:
    def __init__(self, task_store: TaskStore):
        self.task_store = task_store

    def create(self, user_id: str, title: str, description: str) -> TaskData:
        
        if title.strip() == "":
            raise InvalidTaskInput("title")
        if description.strip() == "":
            raise InvalidTaskInput("description")
        
        task_id = str(uuid.uuid4())

        try:
            self.task_store.create(task_id, user_id, title, description, False)
            task = self.task_store.get(task_id)
        except Exception as e:
            raise DatabaseError(e)
        else:
            return task

    def list(self, user_id: str) -> List[TaskData]:
        try:
            tasks = self.task_store.list(user_id)
        except Exception as e:
            raise DatabaseError(e)
        else:
            return tasks

    def update(self, 
               id: str, user_id: str, 
               title: str | None, description: str | None, is_completed: bool | None) -> TaskData:
        task = self.task_store.get(id)
        if task.user_id != user_id:
            raise IlligalUpdate("Only task owner can update the task")

        if title:
            task.title = title
        if description:
            task.description = description
        if is_completed:
            task.is_completed = is_completed

        try:
            self.task_store.update(task)
            updated_task = self.task_store.get(id)
        except Exception as e:
            raise DatabaseError(e)
        else:
            return updated_task