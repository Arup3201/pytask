from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Protocol
from datetime import datetime
from internal.dataclasses import UserData
from internal.dependencies import get_user_service
from internal.exceptions import DatabaseError

class CreateUserRequest(BaseModel):
    display_name: str
    email: str
    password: str

class UserServiceProtocol(Protocol):
    def create(self, display_name: str, email: str, password: str) -> UserData: ...

class CreateUserResponse(BaseModel):
    id: str
    email: str
    display_name: str
    created_at: datetime

class UserController:
    def __init__(self):
        self.router = APIRouter(
            prefix="/users",
            tags=["users"]
        )
        self.__register_routes()

    def __register_routes(self):
        self.router.add_api_route("", self.create, status_code=status.HTTP_201_CREATED)

    def create(self, 
               user: CreateUserRequest, 
               user_service: UserServiceProtocol = Depends(get_user_service)):
        try:
            created_user = user_service.create(user.display_name, user.email, user.password)
        except DatabaseError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User create operation failed. Try again.")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong. We will fix it.")
        else:
            return CreateUserResponse(
                id=created_user.id,
                email=created_user.email,
                display_name=created_user.display_name,
                created_at=created_user.created_at,
            )
