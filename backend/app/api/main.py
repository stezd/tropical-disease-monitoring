from fastapi import APIRouter

from app.api.routes import ai, facilities, login, private, triage, users, utils
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(triage.router)
api_router.include_router(ai.router)
api_router.include_router(facilities.router)


if settings.FASTAPI_ENV == "development":
    api_router.include_router(private.router)
