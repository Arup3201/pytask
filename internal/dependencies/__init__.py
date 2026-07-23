from fastapi import Depends
from sqlalchemy import Engine, create_engine
from internal.config import DatabaseConfig, JWTConfig
from internal.stores.task import TaskStore, SQLAlchemyTaskStorage
from internal.stores.user import UserStore, SQLAlchemyUserStorage
from internal.models.task import TaskService
from internal.models.user import UserService
from internal.utils import TokenUtil

def get_engine() -> Engine:
    engine = create_engine(DatabaseConfig.get_url())
    return engine

def get_task_store(engine: Engine = Depends(get_engine)) -> TaskStore:
    return SQLAlchemyTaskStorage(engine)

def get_task_service(task_store: TaskStore = Depends(get_task_store)) -> TaskService:
    return TaskService(task_store)

def get_user_store(engine: Engine = Depends(get_engine)) -> UserStore:
    return SQLAlchemyUserStorage(engine)

def get_user_service(user_store: UserStore = Depends(get_user_store)) -> UserService:
    return UserService(user_store)

def get_token_util() -> TokenUtil:
    return TokenUtil(JWTConfig.Secret, JWTConfig.Algorithm)
