from typing import Annotated

from fastapi import Depends
from services.film import FilmService as _FilmService
from services.film import get_film_service

FilmService = Annotated[_FilmService, Depends(get_film_service)]
