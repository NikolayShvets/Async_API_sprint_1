from functools import lru_cache
from typing import Any

from elasticsearch import AsyncElasticsearch, NotFoundError
from models import Person, PersonFilm
from services.deps import ElasticClient


class PersonService:
    def __init__(self, elastic: AsyncElasticsearch) -> None:
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
        try:
            doc = await self.elastic.get(index="persons", id=person_id)
        except NotFoundError:
            return None

        return Person(**doc["_source"])

    async def get_films(self, person_id: str, page_size: int, page_number: int) -> list[PersonFilm]:
        person = await self.get_by_id(person_id)

        if not person:
            return []

        return person.films[(page_number - 1) * page_size : page_number * page_size]


@lru_cache(maxsize=1)
def get_person_service(elastic: ElasticClient) -> PersonService:
    return PersonService(elastic)
