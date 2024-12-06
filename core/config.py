from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent
DB_URL = f"{BASE_DIR}/sqlite.db"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{DB_URL}"
    db_echo: bool = True

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
