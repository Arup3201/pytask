from fastapi import FastAPI
from sqlalchemy import create_engine
from internal.config import Config, DatabaseConfig
from internal.stores import Base, User, Task
from internal.controllers.task import task_controller
from internal.controllers.user import auth_controller

app = FastAPI()

Config.load()

engine = create_engine(DatabaseConfig.get_url())
Base.metadata.create_all(engine)

app.include_router(auth_controller.router)
app.include_router(task_controller.router)
