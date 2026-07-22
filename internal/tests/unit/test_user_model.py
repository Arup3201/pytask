import pytest
from typing import List
from datetime import datetime
from internal.dataclasses import UserData
from internal.models.user import UserService, UserStoreProtocol
from internal.exceptions import InvalidUserInput, DatabaseError, NotFound

users: List[UserData] = []

class MockStore:
    def create(self, id: str, email: str,  display_name: str, 
               password_hash: bytes) -> None:
        users.append(UserData(
                id=id,
                email=email,
                display_name=display_name,
                password_hash=password_hash,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ))
    
    def get(self, id: str) -> UserData:
        for u in users:
            if u.id == id:
                return u
        
        raise NotFound("User "+id)

class FaultyMockStore:
    def create(self, id: str, email: str,  display_name: str, 
               password_hash: bytes) -> None:
        raise Exception("Faulty mock store.")

    def get(self, id: str) -> UserData:
        raise Exception("Faulty mock store.")

@pytest.mark.parametrize(
        ("email", "display_name", "password", "store", "raises_db_exception", "raises_invalid_user_exception"), 
        [
            ("test-user@example.com", "test user", "123", 
             MockStore(), False, False),
            ("test-user@example.com", "", "123", 
             MockStore(), False, False),
            ("", "test user", "123", 
             MockStore(), False, True),
            ("test-user@example", "test user", "123", 
             MockStore(), False, True),
            ("test-user.example.com", "test user", "123", 
             MockStore(), False, True),
            ("@example.com", "test user", "123", 
             MockStore(), False, True),
            ("test-user@example.com", "test user", "", 
             MockStore(), False, True),
            ("test-user@example.com", "test user", "123", 
             FaultyMockStore(), True, False),
        ]
)
def test_UserService_create(email: str, 
                            display_name: str, 
                            password: str,
                            store: UserStoreProtocol,
                            raises_invalid_user_exception: bool,
                            raises_db_exception: bool):
    service = UserService(store)

    if raises_invalid_user_exception:
        with pytest.raises(InvalidUserInput):
            service.create(email, display_name, password)
    elif raises_db_exception:
        with pytest.raises(DatabaseError):
            service.create(email, display_name, password)
    else:
        user = service.create(email, display_name, password)
        assert user.email == email
        assert user.display_name == display_name