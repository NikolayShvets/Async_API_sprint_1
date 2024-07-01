import pickle
from uuid import UUID

from redis.asyncio import Redis


class BaseService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self.cache_expire = 300

    @staticmethod
    def _get_complex_id_new(method: str, **kwargs):
        # todo переделать монстра
        return (
            f'{method}:{kwargs.get("item_id")}:{kwargs.get("sort")}:{kwargs.get("genre")}:'
            f'{kwargs.get("page_size")}:{kwargs.get("page_number")}:{kwargs.get("title")}:'
            f'{kwargs.get("name")}:{kwargs.get("role")}:{kwargs.get("film_title")}'
        )

    async def put_item_to_cache(self, method: str, item, **kwargs) -> None:
        print(f"\t Send to cache {method}")
        await self.redis.set(self._get_complex_id_new(method=method, **kwargs), pickle.dumps(item), self.cache_expire)

    async def get_item_from_cache(self, method: str, item_id: UUID | None = None, **kwargs):
        print(f"\n\t Get from cache {method}")
        data = await self.redis.get(self._get_complex_id_new(method=method, item_id=item_id, **kwargs))

        if not data:
            return None

        return pickle.loads(data)
