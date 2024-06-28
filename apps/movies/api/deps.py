from typing import Annotated

from fastapi import Depends
from services.film import FilmService as _FilmService
from services.film import get_film_service
from services.genre import GenreService as _GenreService
from services.genre import get_genre_service

FilmService = Annotated[_FilmService, Depends(get_film_service)]
GenreService = Annotated[_GenreService, Depends(get_genre_service)]
