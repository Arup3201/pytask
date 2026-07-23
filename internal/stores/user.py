from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import Engine, select
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from internal.dataclasses import UserData
from internal.exceptions import NotFound, DuplicateUserEmail
from internal.dataclasses import UserData
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

class UserStore(ABC):
    @abstractmethod
    def create(self, 
               id: str, email: str, display_name: str, 
               password_hash: bytes) -> None: ...
    @abstractmethod
    def get(self, id: str) -> UserData: ...
    @abstractmethod
    def get_by_email(self, email: str) -> UserData: ...


class SQLAlchemyUserStorage(UserStore):
    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, 
               id: str, email: str, display_name: str, 
               password_hash: bytes) -> None:
        
        with Session(self.engine) as session:
            try:
                user = User(id=id, 
                            email=email, 
                            display_name=display_name, 
                            password_hash=password_hash)
                session.add(user)
                session.commit()
            except IntegrityError:
                raise DuplicateUserEmail(email)
            except:
                session.rollback()
                raise
    
    def get(self, id: str) -> UserData:

        with Session(self.engine) as session:


            user = session.get(User, id)
            if user is None:
                raise NotFound(f"User {id}")

            return UserData(
                id=user.id,
                email=user.email,
                display_name=user.display_name,
                password_hash=user.password_hash,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )

    def get_by_email(self, email: str) -> UserData:

        stmt = select(User).where(User.email==email)
        with Session(self.engine) as session:
            user = session.scalar(stmt)
            if user is None:
                raise NotFound(f"Email {email}")
            
            return UserData(
                id=user.id,
                email=user.email,
                display_name=user.display_name,
                password_hash=user.password_hash,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
