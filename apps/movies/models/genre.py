from pydantic import BaseModel


class GenreFilmwork(BaseModel):
    id: str
    title: str
    imdb_rating: float | None


class Genre(BaseModel):
    id: str
    name: str
    description: str | None
    films: list[GenreFilmwork]
