from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from models import Person
from services.deps import ElasticClient

type SearchQuery = dict[
    str, dict[str, dict[str, list[dict[str, dict[str, str | dict[str, str | dict[str, dict[str, str]]]]]]]]
]


class PersonService:
    def __init__(self, elastic: AsyncElasticsearch) -> None:
        self.elastic = elastic

    async def filter(self, name_filter: str | None = None, role_filter: str | None = None) -> list[Person]:
        query: SearchQuery = {"query": {"bool": {"must": []}}}

        if name_filter:
            query["query"]["bool"]["must"].append({"match": {"full_name": name_filter}})
        if role_filter:
            query["query"]["bool"]["must"].append(
                {"nested": {"path": "films", "query": {"match": {"films.roles": role_filter}}}}
            )

        data = await self.elastic.search(index="persons", body=query)

        return [Person(**hit["_source"]) for hit in data["hits"]["hits"]]

    async def get_by_id(self, person_id: str) -> Person | None:
        try:
            doc = await self.elastic.get(index="persons", id=person_id)
        except NotFoundError:
            return None

        return Person(**doc["_source"])


@lru_cache(maxsize=1)
def get_person_service(elastic: ElasticClient) -> PersonService:
    return PersonService(elastic)
