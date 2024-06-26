from uuid import UUID

from schemas.base import BaseSchema


class FilmOutPerson(BaseSchema):
    id: str
    name: str


class FilmOut(BaseSchema):
    id: str
    imdb_rating: float | None
    title: str


class DetailedFilmOut(BaseSchema):
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
