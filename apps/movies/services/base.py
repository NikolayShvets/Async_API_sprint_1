import pickle
from typing import TypeVar
from uuid import UUID

from models import Film, Genre, Person
from redis.asyncio import Redis

ItemModel = TypeVar("ItemModel", Film, Genre, Person)


class BaseService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self.cache_expire = 300

    @staticmethod
    def _get_complex_id(method: str, item: ItemModel | None = None, item_id: UUID | None = None) -> str:
        if not item_id:
            try:
                item_id = item.id
            except AttributeError:
                item_id = None

        return f"{method}:{item_id}"

    async def put_item_to_cache(self, method: str, item: ItemModel) -> None:
        await self.redis.set(self._get_complex_id(method=method, item=item), pickle.dumps(item), self.cache_expire)

    async def get_item_from_cache(self, method: str, item_id: UUID) -> ItemModel | None:
        data = await self.redis.get(self._get_complex_id(method=method, item_id=item_id))
        if not data:
            return None

        return pickle.loads(data)
