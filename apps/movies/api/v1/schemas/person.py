from uuid import UUID

from api.v1.schemas.base import BaseSchema


class PersonSchema(BaseSchema):
    id: UUID
    full_name: str
