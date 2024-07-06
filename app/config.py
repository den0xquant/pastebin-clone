from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_user: str
    database_password: str
    database_name: str
    database_host: str
    database_port: str
    redis_host: str
    redis_port: str

    HASH_LENGTH: int = 20
    HASH_COUNT: int = 10_000
    HASH_LIMIT: int = 100_000
    HASH_KEY: str = 'pastebin'
    REDIS_CACHE_TIMEOUT: int = 10
    REDIS_VIEWS_TO_CACHE: int = 10
    REDIS_CACHE_PREFIX: str = 'paste.cache:'
    REDIS_DELETE_PREFIX: str = 'paste.delete:'
    REDIS_PASTE_VIEWS: str = 'paste.views:'

    @property
    def database_url(self) -> str:
        return "postgresql+asyncpg://%s:%s@%s:%s/%s" % (
            self.database_user, self.database_password,
            self.database_host, self.database_port, self.database_name
        )

    @property
    def redis_url(self) -> str:
        return "redis://%s:%s/0" % (self.redis_host, self.redis_port)


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')  # type: ignore
