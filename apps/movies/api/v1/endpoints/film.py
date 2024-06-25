from api.deps import FilmService
from fastapi import APIRouter, HTTPException, status
from schemas import FilmSchema

router = APIRouter()


@router.get("/{film_id}")
async def film_details(film_id: str, film_service: FilmService) -> FilmSchema:
    """
    Получить информацию о фильме по идентификатору
    """
    film = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Film not found")

    return FilmSchema.model_validate(film)
