from uuid import UUID

from models import Film, Genre, Person
from redis.asyncio import Redis


class BaseService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self.cache_expire = 300

    async def get_item_from_cache(self, item_id: UUID):
        data = await self.redis.get(str(item_id))

        if not data:
            return None

        return data

    async def put_item_to_cache(self, item: Genre | Film | Person):
        await self.redis.set(str(item.id), item.model_dump_json(), self.cache_expire)
