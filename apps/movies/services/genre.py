from functools import lru_cache
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from models import Genre
from services.deps import ElasticClient


class GenreService:
    def __init__(self, elastic: AsyncElasticsearch) -> None:
        self.elastic = elastic

    async def get_by_id(self, genre_id: UUID) -> Genre | None:
        try:
            doc = await self.elastic.get(index="genres", id=str(genre_id))
        except NotFoundError:
            return None

        return Genre(**doc["_source"])


@lru_cache(maxsize=1)
def get_genre_service(elastic: ElasticClient) -> GenreService:
    return GenreService(elastic)
