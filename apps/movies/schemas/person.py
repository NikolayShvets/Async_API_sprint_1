from uuid import UUID

from models.person import PersonRole
from schemas.base import BaseSchema


class PersonSchema(BaseSchema):
    id: UUID
    full_name: str
    role: PersonRole
