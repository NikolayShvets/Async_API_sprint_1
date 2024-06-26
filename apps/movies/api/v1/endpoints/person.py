from uuid import UUID

from api.deps import PersonService
from api.v1.schemas import PersonSchema
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page, paginate

router = APIRouter()


@router.get("/{person_id}")
async def preson_details(person_service: PersonService, person_id: UUID) -> PersonSchema:
    """
    Получить информацию о персоне по идентификатору
    """
    person = await person_service.get_by_id(str(person_id))

    if not person:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Person not found")

    return person


@router.get("/")
async def person_list(
    person_service: PersonService,
    name: str | None = None,
    role: str | None = None,
    film_title: str | None = None,
) -> Page[PersonSchema]:
    """
    Список персон
    """
    persons = await person_service.filter(name, role, film_title)

    return paginate(persons)
