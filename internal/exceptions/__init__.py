class InvalidTaskInput(Exception):
    def __init__(self, property: str):
        self.message = f"Task {property} is invalid"

class DatabaseError(Exception):
    def __init__(self, error: Exception):
        self.message = f"Database operation failed."
        self.error = error
