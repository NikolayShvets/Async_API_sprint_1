from uuid import UUID

from api.v1.schemas.base import BaseSchema


class FilmSchema(BaseSchema):
    id: UUID
    title: str
    imdb_rating: float | None
