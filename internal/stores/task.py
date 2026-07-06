from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Engine
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from internal.dataclasses import TaskData
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

class TaskStore:
    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, 
               id: str, user_id: str, title: str, description: str, 
               is_completed: bool) -> TaskData:

        with Session(self.engine) as session:
            with session.begin():
                task = Task(id=id, 
                    user_id=user_id, 
                    title=title, 
                    description=description, 
                    is_completed=is_completed)
                session.add(task)
        
                return TaskData(
                    id=task.id,
                    user_id=task.user_id,
                    title=task.title,
                    description=task.description,
                    is_completed=task.is_completed,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                )

