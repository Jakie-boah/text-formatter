from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    user: str = Field(alias="DATABASE_USER")
    password: str = Field(alias="DATABASE_PASSWORD")
    host: str = Field(alias="DATABASE_HOST")
    db: str = Field(alias="DATABASE_NAME")
    port: str = Field(alias="DATABASE_PORT", default="5432")

    redis_host: str = Field(default="redis", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")


settings = Settings()
