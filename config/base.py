from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_user: str
    database_password: str
    database_name: str
    database_host: str
    database_port: str
    echo_sql: bool = True
    test: bool = False
    project_name: str = "My FastAPI project"
    oauth_token_secret: str = "my_dev_secret"

    @property
    def database_url(self) -> str:
        return "postgresql+asyncpg://%s:%s@%s:%s/%s" % (
            self.database_user, self.database_password,
            self.database_host, self.database_port, self.database_name
        )


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')  # type: ignore
