import pytest
from pytest import FixtureRequest
from requests import codes, Response
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from internal.stores import Base, User
from internal.config import DatabaseConfig, JWTConfig
from internal.utils import TokenUtil

from testcontainers.postgres import PostgresContainer # type: ignore

from internal.controllers.task import task_controller

postgres = PostgresContainer("postgres:18-alpine")

@pytest.fixture(scope="module")
def get_client() -> TestClient:
    app = FastAPI()
    app.include_router(task_controller.router)
    return TestClient(app)

@pytest.fixture(scope="module")
def get_engine(request: FixtureRequest):
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

@pytest.fixture(scope="module")
def get_token() -> str:
    JWTConfig.Secret = "secret"
    JWTConfig.Algorithm = "HS256"

    return TokenUtil(JWTConfig.Secret, JWTConfig.Algorithm).generate_token("test-user", "test-user@example.com")

def test_TaskController_create(monkeypatch, 
                               get_client: TestClient, 
                               get_token: str, 
                               get_engine: Engine):
    monkeypatch.setattr(DatabaseConfig, "get_url", postgres.get_connection_url)

    response: Response = get_client.post(
        "/tasks/", 
        headers={
            "Content-Type": "application/json", 
            "Authorization": "Bearer "+get_token
        },
        json={
            "title": "Test task", 
            "description": "Test description"
        }
    )

    if response.status_code != codes.CREATED:
        print(response.json())

    assert response.status_code == codes.CREATED

    body = response.json()

    assert body["title"] == "Test task"
    assert body["description"] == "Test description"
