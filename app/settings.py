import os
from pydantic_settings import BaseSettings, SettingsConfigDict

dir_path = os.path.dirname(os.path.realpath(__file__))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(dir_path, ".env"), env_file_encoding="utf-8")

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DB_URL_asyncpg(self):
        # asyncpg://postgres:postgres@localhost:5432/sa
        return f"asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
