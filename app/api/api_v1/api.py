from fastapi import APIRouter
from app.api.api_v1.endpoints import user, request, lookup

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(request.router, prefix="/requests", tags=["requests"])
api_router.include_router(lookup.router, prefix="/lookups", tags=["lookups"])
