from fastapi import APIRouter
from app.api.v1 import auth, content, projects, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(content.router, prefix="/content", tags=["content generation"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])