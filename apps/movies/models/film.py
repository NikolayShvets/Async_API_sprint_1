from pydantic import BaseModel


class FilmPerson(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: float | None
    title: str
    description: str | None
    genres: list[str]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    directors: list[FilmPerson]
    actors: list[FilmPerson]
    writers: list[FilmPerson]
