from uuid import UUID

from api.deps import PersonService
from fastapi import APIRouter, HTTPException, status
from schemas import PersonSchema

router = APIRouter()


@router.get("/{person_id}")
async def preson_details(person_service: PersonService, person_id: UUID) -> PersonSchema:
    """
    Получить информацию о персоне по идентификатору
    """
    person = await person_service.get_by_id(str(person_id))

    if not person:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Person not found")

    return PersonSchema.model_validate(person)


@router.get("/")
async def person_list(
    person_service: PersonService, name: str | None = None, role: str | None = None
) -> list[PersonSchema]:
    """
    Список персон
    """
    persons = await person_service.filter()

    return [PersonSchema.model_validate(person) for person in persons]
