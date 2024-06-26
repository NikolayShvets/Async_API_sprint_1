from typing import Union, Optional
from pydantic import BaseModel, Field


class PersonEntity(BaseModel):
    id: str
    name: str


class Movie(BaseModel):
    id: str
    imdb_rating: Union[float, None]
    title: str
    description: Union[str, None]
    genres: list[str]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    directors: list[PersonEntity]
    actors: list[PersonEntity]
    writers: list[PersonEntity]


class PersonFilmwork(BaseModel):
    id: str
    title: str
    imdb_rating: Union[float, None] = Field(alias='rating')
    roles: list[str]


class Person(BaseModel):
    id: str
    full_name: str
    films: list[PersonFilmwork]


class GenreFilmwork(BaseModel):
    id: str
    title: str
    imdb_rating: Union[float, None] = Field(alias='rating')


class Genre(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    films: list[GenreFilmwork]
