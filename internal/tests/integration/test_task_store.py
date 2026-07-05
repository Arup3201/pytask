import pytest
from pytest import FixtureRequest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from uuid import uuid4
from testcontainers.postgres import PostgresContainer # type: ignore

from internal.stores.base import Base
from internal.stores.task import TaskStore, Task
from internal.stores.user import User

postgres = PostgresContainer("postgres:18-alpine")

@pytest.fixture(scope="module")
def get_engine(request: FixtureRequest) -> Engine:
    postgres.start()

    def cleanup():
        postgres.stop()

    engine = create_engine(postgres.get_connection_url())
    Base.metadata.create_all(engine)

    test_user = User(id="test-user", 
                     email="test-user@example.com", 
                     display_name="test user", 
                     password_hash=("secret key").encode("utf-8"))
    with Session(engine) as session:
        with session.begin():
            session.add(test_user)

    request.addfinalizer(cleanup)
    return engine

def test_TaskStore_create(get_engine: Engine):
    store = TaskStore(get_engine)
    id = str(uuid4())
    task = store.create(id, "test-user", "test task", "test description", False)

    assert task.id == id
    assert task.user_id == "test-user"
    assert task.title == "test task"
    assert task.description == "test description"
    assert task.is_completed == False

    with Session(get_engine) as session:
        with session.begin():
            saved_task = session.get(Task, id)
            
            assert saved_task != None
            assert saved_task.id == id
            assert saved_task.user_id == "test-user"
            assert saved_task.title == "test task"
            assert saved_task.description == "test description"
            assert saved_task.is_completed == False