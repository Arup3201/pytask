import uuid
from typing import Protocol
from internal.dataclasses import TaskData
from internal.exceptions import InvalidTaskInput, DatabaseError

# Structural subtyping 
# https://realpython.com/python-interface/#defining-a-protocol-based-interface
class TaskStoreProtocol(Protocol):
    def create(self, 
               id: str, user_id: str, title: str, description: str, 
               is_completed: bool) -> TaskData:
        ...

class TaskService:
    def __init__(self, task_store: TaskStoreProtocol):
        self.task_store = task_store

    def create(self, user_id: str, title: str, description: str) -> TaskData:
        
        if title.strip() == "":
            raise InvalidTaskInput("title")
        if description.strip() == "":
            raise InvalidTaskInput("description")
        
        task_id = str(uuid.uuid4())

        try:
            task = self.task_store.create(task_id, user_id, title, description, False)
        except Exception as e:
            raise DatabaseError(e)
        else:
            return task