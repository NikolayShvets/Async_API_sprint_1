from functools import lru_cache
from typing import Any
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from models import Genre
from redis.asyncio import Redis
from services.deps import ElasticClient, RedisClient

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService:
    def __init__(self, elastic: AsyncElasticsearch, redis: Redis) -> None:
        self.elastic = elastic
        self.redis = redis

    async def get_by_id(self, genre_id: UUID) -> Genre | None:
        genre = await self._genre_from_cache(genre_id)

        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None

            await self._put_film_to_cache(genre)

        return genre

    async def get_all_genres(self) -> list[Genre]:
        query: dict[str, Any] = {"query": {"bool": {"must": []}}}
        data = await self.elastic.search(index="genres", body=query)

        return [Genre(**hit["_source"]) for hit in data["hits"]["hits"]]

    async def _genre_from_cache(self, genre_id: UUID) -> Genre | None:
        data = await self.redis.get(str(genre_id))
        if not data:
            return None

        genre = Genre.model_validate_json(data)
        return genre

    async def _put_film_to_cache(self, genre: Genre):
        await self.redis.set(str(genre.id), genre.model_dump_json(), FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _get_genre_from_elastic(self, genre_id: UUID) -> Genre | None:
        try:
            doc = await self.elastic.get(index="genres", id=str(genre_id))
        except NotFoundError:
            return None

        return Genre(**doc["_source"])


@lru_cache(maxsize=1)
def get_genre_service(elastic: ElasticClient, redis: RedisClient) -> GenreService:
    return GenreService(elastic, redis)
