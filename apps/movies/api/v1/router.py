from api.v1.endpoints.film import router as film_router
from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")


api_router.include_router(film_router, prefix="/films", tags=["Films"])
