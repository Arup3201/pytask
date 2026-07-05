from internal.models.task import TaskService, TaskStoreProtocol, DatabaseError, InvalidTaskInput
from internal.dcs.dataclasses import TaskData
from datetime import datetime
from dataclasses import dataclass
import pytest

@dataclass
class CreateTaskData:
    user_id: str
    title: str
    description: str
    store: TaskStoreProtocol
    raises_db_exception: bool = False

class MockStore:
    def create(self, id: str, user_id: str,  title: str, description: str, 
               is_completed: bool) -> TaskData:
        return TaskData(id=id, 
                        user_id=user_id,
                        title=title, 
                        description=description, 
                        is_completed=is_completed, 
                        created_at=datetime.now(), 
                        updated_at=datetime.now())

class FaultyMockStore:
    def create(self, id: str, user_id: str,  title: str, description: str, 
               is_completed: bool) -> TaskData:
        raise Exception("Faulty mock store.")

@pytest.mark.parametrize(
        ("user_id", "task_title", "task_description", "store", "raises_db_exception", "raises_invalid_task_exception"), 
        [
            ("test-user", "test title", "test description", 
             MockStore(), False, False),
            ("test-user", "test title", "test description", 
             FaultyMockStore(), True, False),
            ("test-user", "", "test description", 
             FaultyMockStore(), False, True),
            ("test-user", "test title", "", 
             FaultyMockStore(), False, True),
        ]
)
def test_TaskService_create(user_id: str, 
                            task_title: str, 
                            task_description: str, 
                            store: TaskStoreProtocol,
                            raises_invalid_task_exception: bool,
                            raises_db_exception: bool):
    service = TaskService(store)

    if raises_invalid_task_exception:
        with pytest.raises(InvalidTaskInput):
            service.create(user_id, task_title, task_description)
    elif raises_db_exception:
        with pytest.raises(DatabaseError):
            service.create(user_id, task_title, task_description)
    else:
        task = service.create(user_id, task_title, task_description)
        assert task.id.strip() != ""
        assert task.user_id == user_id
        assert task.title == task_title
        assert task.description == task_description
        assert task.is_completed == False

