import uuid
from typing import List
from internal.dataclasses import TaskData
from internal.exceptions import InvalidTaskInput, DatabaseError
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
