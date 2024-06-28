from uuid import UUID

from api.deps import GenreService
from fastapi import APIRouter, HTTPException, status
from models import Genre
from schemas import GenreSchema

router = APIRouter()


@router.get("/{genre_id}", response_model=GenreSchema)
async def genre_by_id(genre_id: UUID, genre_service: GenreService) -> Genre:
    genre = await genre_service.get_by_id(genre_id)

    if not genre:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Genre not found")

    return genre


@router.get("/")
async def genre_list(genre_service: GenreService) -> list[GenreSchema]:
    genres = await genre_service.get_all_genres()

    return genres
