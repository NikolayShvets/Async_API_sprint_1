from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from models import Film
from models.genre import Genre
from redis.asyncio import Redis
from services.deps import ElasticClient, RedisClient


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Film | None:
        film = await self._get_film_from_elastic(film_id)
        if not film:
            return None

        return film

    async def get_all(
        self,
        sort: str | None,
        genre: str | None,
        page_size: int,
        page_number: int,
    ):
        sort_conf = self._get_sort_conf(sort)
        query = await self._get_genre_filter_query(genre)

        return await self._get_films_from_elastic(
            search_size=page_size,
            search_from=(page_number - 1) * page_size,
            sort=sort_conf,
            query=query
        )

    async def search(
        self,
        title: str,
        page_size: int,
        page_number: int,
    ):
        return await self._get_films_from_elastic(
            search_size=page_size,
            search_from=(page_number - 1) * page_size,
            query={'match': {'title': title}},
        )

    def _get_sort_conf(self, sort: str | None):
        if not sort:
            return None

        sort_order = sort[0:1]

        if sort_order.startswith('-'):
            sort_key = sort[1:]
            order = 'asc'
            mode = 'min'
        else:
            sort_key = sort
            order = 'desc'
            mode = 'max'

        return {sort_key: {'order': order, 'mode': mode}}

    async def _get_genre_filter_query(self, genre: str | None):
        if not genre:
            return None

        try:
            doc = await self.elastic.get(index="genres", id=genre)
        except NotFoundError:
            return None

        genre_name = Genre(**doc['_source']).name

        return {
            'bool': {
                'filter': [
                    {'term': {'genres': genre_name}},
                ],
            },
        }

    async def _get_film_from_elastic(self, film_id: str) -> Film | None:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])

    async def _get_films_from_elastic(
        self,
        search_size: int,
        search_from: int,
        sort: dict | None = None,
        query: dict | None = None
    ):
        search_body: dict[str, int | dict] = {
            'size': search_size,
            'from': search_from,
        }

        if sort:
            search_body['sort'] = sort
        if query:
            search_body['query'] = query

        try:
            doc = await self.elastic.search(index="movies", body=search_body)
        except NotFoundError:
            return None

        return [
            Film(**hit['_source'])
            for hit in doc['hits']['hits']
        ]


@lru_cache(maxsize=1)
def get_film_service(redis: RedisClient, elastic: ElasticClient) -> FilmService:
    return FilmService(redis, elastic)
