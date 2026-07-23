from typing import Protocol
import uuid, bcrypt, re
from internal.dataclasses import UserData
from internal.exceptions import InvalidUserInput, InvalidEmail, IncorrectPassword, DatabaseError, NotFound
from internal.stores.user import UserStore

class UserService:
    def __init__(self, user_store: UserStore):
        self.user_store = user_store

    def create(self, email: str, display_name: str, password: str) -> UserData:
        user_id = str(uuid.uuid4())

        if not bool(re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)):
            raise InvalidUserInput("email")

        if password.strip() == "":
            raise InvalidUserInput("password")
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))

        try:
            self.user_store.create(user_id, email, display_name, hashed)
            user = self.user_store.get(user_id)
        except Exception as e:
            raise DatabaseError(e)
        else:
            return user

    def get_user_by_email_password(self, email: str, password: str) -> UserData:
        try:
            user = self.user_store.get_by_email(email)

            if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
                raise IncorrectPassword

        except NotFound:
            raise InvalidEmail
        except Exception as e:
            raise DatabaseError(e)
        else:
            return user