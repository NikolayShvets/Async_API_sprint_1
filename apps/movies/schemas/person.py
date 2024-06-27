from uuid import UUID
from schemas.base import BaseSchema


class PersonSchema(BaseSchema):
    id: UUID
    full_name: str
