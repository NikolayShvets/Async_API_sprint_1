from schemas.base import BaseModel


class FilmOutPerson(BaseModel):
    id: str
    name: str


class FilmOut(BaseModel):
    id: str
    imdb_rating: float | None
    title: str


class DetailedFilmOut(BaseModel):
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
