import os

class DatabaseConfig:
    Host: str
    Port: str
    User: str
    Password: str
    Database: str

    @classmethod
    def get_url(cls) -> str:
        return f"postgresql://{cls.User}:{cls.Password}@{cls.Host}:{cls.Port}/{cls.Database}"
    
class JWTConfig:
    Secret: str
    Algorithm: str

class Config:

    @staticmethod   
    def load():
        user = os.getenv("DB_USER")
        if user is None:
            raise ValueError("DB_USER is required")
        DatabaseConfig.User = user

        password = os.getenv("DB_PASSWORD")
        if password is None:
            raise ValueError("DB_PASSWORD is required")
        DatabaseConfig.Password = password

        database = os.getenv("DB_NAME")
        if database is None:
            raise ValueError("DB_NAME is required")
        DatabaseConfig.Database = database

        host = os.getenv("DB_HOST")
        if host is None:
            print("DB_HOST not found. DEFAULT: localhost")
            DatabaseConfig.Host = "localhost"
        else:
            DatabaseConfig.Host = host
        
        port = os.getenv("DB_PORT")
        if port is None:
            print("DB_PORT not found. DEFAULT: 5432")
            DatabaseConfig.Port = "5432"
        else:
            DatabaseConfig.Port = port

        jwt_secret = os.getenv("JWT_SECRET")
        if jwt_secret is None:
            raise ValueError("JWT_SECRET is required")
        JWTConfig.Secret = jwt_secret

        jwt_algorithm = os.getenv("JWT_ALGORITHM")
        if jwt_algorithm is None:
            print("JWT_ALGORITHM not found. DEFAULT: HS256")
            JWTConfig.Algorithm = "HS256"
        else:
            JWTConfig.Algorithm = jwt_algorithm
