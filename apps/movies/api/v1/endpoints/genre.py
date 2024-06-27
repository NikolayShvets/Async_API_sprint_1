from uuid import UUID

from api.deps import GenreService
from fastapi import APIRouter, HTTPException, status
from schemas import GenreSchema

router = APIRouter()


@router.get("/{genre_id}")
async def genre_by_id(genre_id: UUID, genre_service: GenreService) -> GenreSchema:
    genre = await genre_service.get_by_id(genre_id)

    if not genre:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Genre not found")

    return GenreSchema.model_validate(genre)


@router.get("/")
async def genre_list(genre_service: GenreService) -> list[GenreSchema]:
    genres = await genre_service.get_all_genres()

    return genres
