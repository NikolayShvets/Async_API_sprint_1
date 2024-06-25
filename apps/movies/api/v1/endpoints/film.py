from api.deps import FilmService
from fastapi import APIRouter, HTTPException, status, Depends
from schemas.film import FilmOut, GetFilmsQueryParams
from typing import Annotated

router = APIRouter()


@router.get("/{film_id}", response_model=FilmOut)
async def film_details(
    film_id: str,
    film_service: FilmService
) -> FilmOut:
    """
    Получить информацию о фильме по идентификатору
    """
    film = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Film not found")

    return FilmOut(**film.model_dump())


@router.get("/", response_model=list[FilmOut])
async def get_films(
    film_service: FilmService,
    query: Annotated[GetFilmsQueryParams, Depends()],
):
    films = await film_service.get_all(
        sort=query.sort,
        genre=query.genre,
        page_size=query.page_size,
        page_number=query.page_number
    )
    return films
