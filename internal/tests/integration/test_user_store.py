import pytest
from pytest import FixtureRequest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from uuid import uuid4
from testcontainers.postgres import PostgresContainer # type: ignore

from internal.stores.base import Base
from internal.stores.user import UserStore, User
from internal.stores.task import Task

postgres = PostgresContainer("postgres:18-alpine")

@pytest.fixture(scope="module")
def get_engine(request: FixtureRequest) -> Engine:
    postgres.start()

    def cleanup():
        postgres.stop()

    engine = create_engine(postgres.get_connection_url())
    Base.metadata.create_all(engine)

    request.addfinalizer(cleanup)
    return engine

def test_UserStore_create(get_engine: Engine):
    store = UserStore(get_engine)
    test_id = str(uuid4())
    test_email = "test-user@example.com"
    test_name = "test user"
    test_password = "123".encode("utf-8")
    store.create(test_id, test_email, test_name, test_password)

    with Session(get_engine) as session:
        user = session.get(User, test_id)

        assert user is not None    
        assert user.id == test_id
        assert user.email == test_email
        assert user.display_name == test_name
        assert user.password_hash == test_password
