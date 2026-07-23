class InvalidUserInput(BaseException):
    def __init__(self, property: str):
        self.message = f"User {property} is invalid."

class InvalidEmail(BaseException):
    def __init__(self):
        self.message = f"Email is invalid."

class IncorrectPassword(BaseException):
    def __init__(self):
        self.message = f"Password is wrong."

class DuplicateUserEmail(BaseException):
    def __init__(self, email: str):
        self.message = f"Email {email} already exists."

class InvalidTaskInput(BaseException):
    def __init__(self, property: str):
        self.message = f"Task {property} is invalid."

class DatabaseError(BaseException):
    def __init__(self, error: BaseException):
        self.message = f"Database operation failed."
        self.error = error

class TokenVerificationError(BaseException):
    def __init__(self, msg: str):
        self.message = f"Token verification error. "+msg

class NotFound(BaseException):
    def __init__(self, msg: str):
        self.message = f"Resource not found. "+msg