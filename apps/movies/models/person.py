from enum import StrEnum, auto
from uuid import UUID

from pydantic import BaseModel


class PersonRole(StrEnum):
    ACTOR = auto()
    DIRECTOR = auto()
    WRITER = auto()


class Person(BaseModel):
    id: UUID
    full_name: str
    role: PersonRole
