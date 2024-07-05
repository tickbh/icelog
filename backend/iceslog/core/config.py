
from typing import Union
from pydantic import HttpUrl, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True, extra="ignore"
    )
    FIRST_SUPER_USER: str = "admin"
    FIRST_SUPER_PASS: str = "123456"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    SECRET_KEY: str = "change this secert"
    
    SQLITE_NAME: Union[str, None] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12
    
    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> Union[PostgresDsn, HttpUrl, str]:
        if self.SQLITE_NAME:
            return f"sqlite:///{self.SQLITE_NAME}"
        else:
            raise Exception("aaa")
            # return MultiHostUrl.build(
            #     scheme="postgresql+psycopg",
            #     username=self.POSTGRES_USER,
            #     password=self.POSTGRES_PASSWORD,
            #     host=self.POSTGRES_SERVER,
            #     port=self.POSTGRES_PORT,
            #     path=self.POSTGRES_DB,
            # )


settings = Settings()  # type: ignore