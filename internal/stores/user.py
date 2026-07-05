from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .task import Task

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    display_name: Mapped[Optional[str]]
    password_hash: Mapped[bytes]

    tasks: Mapped[List["Task"]] = relationship(back_populates="user")