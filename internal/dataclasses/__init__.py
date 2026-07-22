from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TaskData:
    id: str
    user_id: str
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class JWTClaim:
    sub: str
    email: str

@dataclass
class UserData:
    id: str
    email: str
    display_name: str | None
    password_hash: bytes = field(repr=False)
    created_at: datetime
    updated_at: datetime
