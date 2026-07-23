from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Protocol, Annotated
from datetime import datetime
from internal.dataclasses import UserData
from internal.dependencies import get_user_service, get_token_util
from internal.utils import TokenUtil
from internal.exceptions import InvalidUserInput, DatabaseError, TokenVerificationError
from internal.models.user import UserService

class RegisterRequest(BaseModel):
    display_name: str
    email: str
    password: str

class RegisterResponse(BaseModel):
    id: str
    email: str
    display_name: str | None
    created_at: datetime
    updated_at: datetime

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    expires_at: datetime
    user: UserData

class AuthController:
    def __init__(self):
        self.router = APIRouter(
            prefix="/auth",
            tags=["auth"]
        )
        self.__register_routes()

    def __register_routes(self):
        self.router.add_api_route("/register", 
                                  self.register, 
                                  methods=["POST"], 
                                  status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/login", 
                                  self.login, 
                                  methods=["POST"], 
                                  status_code=status.HTTP_200_OK)

    def register(self, 
               user: RegisterRequest, 
               user_service: Annotated[UserService, Depends(get_user_service)]):
        try:
            created_user = user_service.create(user.email, user.display_name, user.password)
        except InvalidUserInput as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="User email/password is invalid.")
        except DatabaseError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail="User create operation failed. Try again.")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail="Something went wrong. We are fixing it.")
        else:
            return RegisterResponse(
                id=created_user.id,
                email=created_user.email,
                display_name=created_user.display_name,
                created_at=created_user.created_at,
                updated_at=created_user.updated_at,
            )

    def login(self, 
              payload: LoginRequest, 
              user_service: Annotated[UserService, Depends(get_user_service)], 
              token_util: TokenUtil = Depends(get_token_util)):
        try:
            user = user_service.get_user_by_email_password(payload.email, payload.password)
            access_token, expires_at = token_util.generate_token(user.id, user.email)
        except TokenVerificationError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Invalid auth token has been provided.")
        except DatabaseError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail="Database check failed. Please try again.")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail="Something went wrong.  We are fixing it.")
        else:
            return LoginResponse(access_token=access_token, expires_at=expires_at, user=user)

auth_controller = AuthController()