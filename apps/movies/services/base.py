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

    # @staticmethod
    # def _get_complex_id(method: str, item: ItemModel | None = None, item_id: UUID | None = None) -> str:
    #     if item_id is None and item is not None:
    #         item_id = getattr(item, "id", None)
    #
    #     return f"{method}:{item_id}" if item_id else f"{method}:None"

    @staticmethod
    def _get_complex_id_new(method: str, **kwargs):
        return (
            f'{method}:{kwargs.get("item_id")}:{kwargs.get("sort")}:{kwargs.get("genre")}:'
            f'{kwargs.get("page_size")}:{kwargs.get("page_number")}:{kwargs.get("title")}'
        )

    async def put_item_to_cache(self, method: str, item: ItemModel | list[ItemModel], **kwargs) -> None:
        print(f"\t Send to cache {method}")
        await self.redis.set(self._get_complex_id_new(method=method, **kwargs), pickle.dumps(item), self.cache_expire)

    async def get_item_from_cache(self, method: str, item_id: UUID | None = None, **kwargs) -> ItemModel | None:
        print(f"\n\t Get from cache {method}")
        data = await self.redis.get(self._get_complex_id_new(method=method, item_id=item_id, **kwargs))

        if not data:
            return None

        return pickle.loads(data)
