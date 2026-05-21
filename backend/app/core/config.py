"""Application settings via environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MIMO_API_KEY: str = ""
    MIMO_BASE_URL: str = "https://api.xiaomimimo.com/v1"
    MIMO_MODEL: str = "mimo-v2.5-pro"
    MIMO_VL_MODEL: str = "mimo-v2.5-vl"
    DAILY_TOKEN_BUDGET: int = 10_000_000
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: str = ".py,.js,.ts,.go,.rs,.java,.c,.cpp,.rb,.php,.pdf,.txt,.csv,.json,.md,.html,.css,.png,.jpg,.jpeg,.webp"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
