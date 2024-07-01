import pickle

from redis.asyncio import Redis


class BaseService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self.cache_expire = 300

    @staticmethod
    def _get_complex_id(method, item) -> str:
        try:
            item_id = item.id
        except AttributeError:
            item_id = None

        return f"{method}:{item_id}"

    async def put_item_to_cache(self, method, item):
        await self.redis.set(self._get_complex_id(method, item), pickle.dumps(item), self.cache_expire)

    async def get_item_from_cache(self, method, item_id):
        data = await self.redis.get(self._get_complex_id(method, item_id))
        if not data:
            return None

        return pickle.loads(data)
