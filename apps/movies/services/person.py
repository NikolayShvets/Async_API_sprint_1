from functools import lru_cache
from typing import Any

from elasticsearch import AsyncElasticsearch, NotFoundError
from models import Person, PersonFilm
from redis.asyncio import Redis
from services.deps import ElasticClient, RedisClient

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class PersonService:
    def __init__(self, elastic: AsyncElasticsearch, redis: Redis) -> None:
        self.redis = redis
        self.elastic = elastic

    async def search(
        self,
        page_size: int,
        page_number: int,
        name: str | None = None,
        role: str | None = None,
        film_title: str | None = None,
    ) -> list[Person]:
        query: dict[str, Any] = {"query": {"bool": {"must": []}}}

        query["from"] = (page_number - 1) * page_size
        query["size"] = page_size

        if name:
            query["query"]["bool"]["must"].append({"match": {"full_name": name}})
        if role:
            query["query"]["bool"]["must"].append(
                {"nested": {"path": "films", "query": {"match": {"films.roles": role}}}}
            )
        if film_title:
            query["query"]["bool"]["must"].append(
                {"nested": {"path": "films", "query": {"match": {"films.title": film_title}}}}
            )

        data = await self.elastic.search(index="persons", body=query)

        return [Person(**hit["_source"]) for hit in data["hits"]["hits"]]

    async def get_by_id(self, person_id: str) -> Person | None:
        person = await self._person_from_cache(person_id)

        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None

            await self._put_person_to_cache(person)

        return person

    async def get_films(self, person_id: str, page_size: int, page_number: int) -> list[PersonFilm]:
        person = await self.get_by_id(person_id)

        if not person:
            return []

        return person.films[(page_number - 1) * page_size : page_number * page_size]

    async def _get_person_from_elastic(self, person_id: str) -> Person | None:
        try:
            doc = await self.elastic.get(index="persons", id=str(person_id))
        except NotFoundError:
            return None

        return Person(**doc["_source"])

    async def _person_from_cache(self, person_id: str) -> Person | None:
        data = await self.redis.get(person_id)
        if not data:
            return None

        genre = Person.model_validate_json(data)
        return genre

    async def _put_person_to_cache(self, person: Person) -> None:
        await self.redis.set(str(person.id), person.model_dump_json(), FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache(maxsize=1)
def get_person_service(elastic: ElasticClient, redis: RedisClient) -> PersonService:
    return PersonService(elastic, redis)
