from collections.abc import AsyncGenerator
from fastapi import Depends
from sqlalchemy import Engine, create_engine
from internal.config import DatabaseConfig, JWTConfig
from internal.stores.task import TaskStore
from internal.models.task import TaskService
from internal.utils import TokenUtil

def get_engine() -> Engine:
    engine = create_engine(DatabaseConfig.get_url())
    return engine

def get_task_store(engine: Engine = Depends(get_engine)) -> TaskStore:
    return TaskStore(engine)

def get_task_service(task_store: TaskStore = Depends(get_task_store)) -> TaskService:
    return TaskService(task_store)

def get_token_util() -> TokenUtil:
    return TokenUtil(JWTConfig.Secret, JWTConfig.Algorithm)
