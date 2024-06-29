from uuid import UUID

from models import Film, Genre, Person
from pydantic import BaseModel
from redis.asyncio import Redis


class BaseService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self.cache_expire = 300

    async def get_item_from_cache(self, item_id: UUID, item_model: type[BaseModel]):
        data = await self.redis.get(str(item_id))

        if not data:
            return None

        data = item_model.model_validate_json(data)
        return data

    async def put_item_to_cache(self, item: Genre | Film | Person) -> None:
        await self.redis.set(str(item.id), item.model_dump_json(), self.cache_expire)
