from uuid import UUID

from schemas.base import BaseSchema


class GenreSchema(BaseSchema):
    id: UUID
    name: str
