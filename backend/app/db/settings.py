from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    test_database_url: str
    pool_size: int
    max_overflow: int
    pool_timeout: int
    pool_recycle: int
    pool_pre_ping: bool


settings = Settings()
