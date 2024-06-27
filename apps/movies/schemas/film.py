from uuid import UUID

from schemas.base import BaseSchema


class FilmSchema(BaseSchema):
    id: UUID
    title: str
