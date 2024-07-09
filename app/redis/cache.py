import json

import redis.asyncio as redis

from app.config import settings
from app.models.schemas import PasteSchema, Expiration, ExpirationMapping


def get_cache_key(paste_hash_id: str) -> str:
    return f"{settings.REDIS_CACHE_PREFIX}{paste_hash_id}"


def get_delete_key(paste_hash_id: str) -> str:
    return f"{settings.REDIS_DELETE_PREFIX}{paste_hash_id}"


def get_views_key(paste_hash_id: str) -> str:
    return f"{settings.REDIS_PASTE_VIEWS}{paste_hash_id}"


class PastebinRedis(redis.Redis):
    async def set_paste_expiration(self, paste: PasteSchema):
        key = get_delete_key(paste.hash_id)
        expiration = ExpirationMapping.get(paste.expiration.name)
        if paste.expiration != Expiration.NEVER:
            await self.set(key, paste.id, ex=expiration)

    async def set_paste_cache(self, paste: PasteSchema):
        key = get_cache_key(paste.hash_id)
        data = json.dumps(
            {
                **paste.dict(),
                'exposure': paste.exposure.value,
                'category': paste.category.value,
                'expiration': paste.expiration.name,
            },
            default=str,
        )
        await self.set(key, data, ex=settings.REDIS_CACHE_TIMEOUT)

    async def get_paste_by_hash_id(self, hash_id: str) -> PasteSchema | None:
        cached_paste = await self.get(get_cache_key(hash_id))
        if cached_paste:
            data = json.loads(cached_paste)
            data.update({'expiration': Expiration.__members__.get(data['expiration'])})
            return PasteSchema(**data)

    async def incr_paste_views(self, hash_id: str):
        await self.incr(get_views_key(hash_id))

    async def set_paste_views(self, hash_id: str):
        await self.set(get_views_key(hash_id), 0)
