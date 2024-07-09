from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    REDIS_HOST: str
    REDIS_PORT: str

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
            self.DATABASE_USER, self.DATABASE_PASSWORD,
            self.DATABASE_HOST, self.DATABASE_PORT, self.DATABASE_NAME
        )

    @property
    def redis_url(self) -> str:
        return "redis://%s:%s/0" % (self.REDIS_HOST, self.REDIS_PORT)


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')  # type: ignore
