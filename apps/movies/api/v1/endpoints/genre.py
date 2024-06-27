from uuid import UUID

from api.deps import GenreService
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get("/")
async def genre_list(genre_service: GenreService, genre_id: UUID):
    genre = await genre_service.get_by_id(genre_id)

    if not genre:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Genre not found")

    return genre
