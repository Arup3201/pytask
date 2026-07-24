class InvalidUserInput(Exception):
    def __init__(self, property: str):
        self.message = f"User {property} is invalid."
        super().__init__(self.message)

class InvalidEmail(Exception):
    def __init__(self):
        self.message = f"Email is invalid."
        super().__init__(self.message)

class IncorrectPassword(Exception):
    def __init__(self):
        self.message = f"Password is wrong."
        super().__init__(self.message)

class DuplicateUserEmail(Exception):
    def __init__(self, email: str):
        self.message = f"Email {email} already exists."
        super().__init__(self.message)

class InvalidTaskInput(Exception):
    def __init__(self, property: str):
        self.message = f"Task {property} is invalid."
        super().__init__(self.message)

class IlligalUpdate(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DatabaseError(Exception):
    def __init__(self, error: Exception):
        self.message = f"Database operation failed."
        self.error = error
        super().__init__(self.message)

class TokenVerificationError(Exception):
    def __init__(self, msg: str):
        self.message = f"Token verification error. "+msg
        super().__init__(self.message)

class NotFound(Exception):
    def __init__(self, msg: str):
        self.message = f"Resource not found. "+msg
        super().__init__(self.message)
