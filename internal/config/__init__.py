
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
