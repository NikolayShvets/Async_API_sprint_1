from typing import Optional
from schemas.base import BaseModel


class FilmOutPerson(BaseModel):
    id: str
    name: str


class GetFilmsQueryParams(BaseModel):
    sort: str | None = None
    genre: str | None = None
    page_size: int = 2
    page_number: int = 1


class FilmOut(BaseModel):
    id: str
    imdb_rating: float | None
    title: str
    description: str | None
    genres: list[str]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    directors: list[FilmOutPerson]
    actors: list[FilmOutPerson]
    writers: list[FilmOutPerson]
