from dataclasses import dataclass
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
