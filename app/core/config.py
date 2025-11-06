from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import BaseModel


BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "app" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "app" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///database.db"
    SECRET_KEY: str = "FkvnicDZt45Jzosuu5XlOa1MxvKrkH6S"
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()