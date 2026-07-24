from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, String, Engine, select, update, delete
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from internal.dataclasses import TaskData
from internal.dataclasses import TaskData
from internal.exceptions import NotFound
from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .user import User

class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(128))
    is_completed: Mapped[bool]

    user: Mapped["User"] = relationship(back_populates="tasks")

class TaskStore(ABC):
    @abstractmethod
    def create(self, 
               id: str, user_id: str, title: str, description: str, 
               is_completed: bool) -> None: ...
    @abstractmethod
    def get(self, id: str) -> TaskData: ...

    @abstractmethod
    def list(self, user_id: str) -> List[TaskData]: ...

    @abstractmethod
    def update(self, task: TaskData) -> None: ...

    @abstractmethod
    def delete(self, id: str) -> None: ...

class SQLAlchemyTaskStorage(TaskStore):
    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, 
               id: str, user_id: str, title: str, description: str, 
               is_completed: bool) -> None:

        with Session(self.engine) as session:
            try:
                task = Task(id=id, 
                    user_id=user_id, 
                    title=title, 
                    description=description, 
                    is_completed=is_completed)
                session.add(task)
                session.commit()
            except:
                session.rollback()
                raise

    def get(self, id: str) -> TaskData:

        with Session(self.engine) as session:
            task = session.get(Task, id)
            
            if task is None:
                raise NotFound("Task "+id)
            
            return TaskData(
                    id=task.id,
                    user_id=task.user_id,
                    title=task.title,
                    description=task.description,
                    is_completed=task.is_completed,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                )

    def list(self, user_id: str) -> List[TaskData]:

        with Session(self.engine) as session:
            stmt = select(Task).where(Task.user_id == user_id)
            rows = session.execute(stmt).scalars()

            tasks: List[TaskData] = []
            for r in rows:
                tasks.append(TaskData(
                    id=r.id,
                    user_id=r.user_id,
                    title=r.title,
                    description=r.description,
                    is_completed=r.is_completed,
                    created_at=r.created_at,
                    updated_at=r.updated_at,
                ))
            return tasks

    def update(self, task: TaskData) -> None:

        with Session(self.engine) as session:
            try:
                stmt = update(Task).where(Task.id == task.id).values(
                    title=task.title, 
                    description=task.description, 
                    is_completed=task.is_completed
                )
                session.execute(stmt)
                session.commit()
            except:
                session.rollback()
                raise
    def delete(self, id: str) -> None:

        with Session(self.engine) as session:
            try:
                stmt = delete(Task).where(Task.id == id)
                session.execute(stmt)
                session.commit()
            except:
                session.rollback()