class InvalidUserInput(Exception):
    def __init__(self, property: str):
        self.message = f"User {property} is invalid"

class DuplicateUserEmail(Exception):
    def __init__(self, email: str):
        self.message = f"Email {email} already exists"

class InvalidTaskInput(Exception):
    def __init__(self, property: str):
        self.message = f"Task {property} is invalid"

class DatabaseError(Exception):
    def __init__(self, error: Exception):
        self.message = f"Database operation failed."
        self.error = error

class TokenVerificationError(Exception):
    def __init__(self, msg: str):
        self.message = f"Token verification error. "+msg

class NotFound(Exception):
    def __init__(self, msg: str):
        self.message = f"Resource not found. "+msg