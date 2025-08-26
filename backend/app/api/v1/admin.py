from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...core.database import get_db
from ...models.user import User
from ...services.api_key_manager import api_key_manager
from .auth import get_current_active_user

router = APIRouter()

class APIKeyStatus(BaseModel):
    total_keys: int
    active_keys: int
    rate_limited_keys: int
    error_keys: int
    keys: List[dict]

class SystemStats(BaseModel):
    total_users: int
    active_users: int
    total_projects: int
    total_generations: int
    api_key_status: APIKeyStatus

def get_admin_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    """Dependency to ensure user is admin"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/api-keys/status", response_model=APIKeyStatus)
def get_api_key_status(
    admin_user: Annotated[User, Depends(get_admin_user)]
):
    """Get status of all API keys"""
    status = api_key_manager.get_status_summary()
    return APIKeyStatus(**status)

@router.post("/api-keys/rotate")
def rotate_api_key(
    admin_user: Annotated[User, Depends(get_admin_user)]
):
    """Force rotation to next available API key"""
    current_key = api_key_manager.get_current_key()
    next_key = api_key_manager.get_next_key()
    
    if not next_key:
        raise HTTPException(status_code=400, detail="No available API keys to rotate to")
    
    return {
        "message": "API key rotated successfully",
        "previous_key": current_key[-8:] if current_key else None,
        "current_key": next_key[-8:] if next_key else None
    }

@router.post("/api-keys/{key_index}/reset")
def reset_api_key_status(
    key_index: int,
    admin_user: Annotated[User, Depends(get_admin_user)]
):
    """Reset status of a specific API key"""
    if key_index < 1 or key_index > len(api_key_manager.api_keys):
        raise HTTPException(status_code=400, detail="Invalid key index")
    
    # Reset key status
    status = api_key_manager.key_status[key_index - 1]
    status['active'] = True
    status['rate_limit_reset'] = None
    status['error_count'] = 0
    status['last_error'] = None
    
    return {"message": f"API key {key_index} status reset successfully"}

@router.get("/stats", response_model=SystemStats)
def get_system_stats(
    admin_user: Annotated[User, Depends(get_admin_user)],
    db: Session = Depends(get_db)
):
    """Get system statistics"""
    from ...models.project import Project
    from ...models.content import ContentGeneration
    
    # Get user stats
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    
    # Get project stats
    total_projects = db.query(Project).count()
    
    # Get generation stats
    total_generations = db.query(ContentGeneration).count()
    
    # Get API key status
    api_key_status = api_key_manager.get_status_summary()
    
    return SystemStats(
        total_users=total_users,
        active_users=active_users,
        total_projects=total_projects,
        total_generations=total_generations,
        api_key_status=APIKeyStatus(**api_key_status)
    )

@router.get("/users", response_model=List[dict])
def get_all_users(
    admin_user: Annotated[User, Depends(get_admin_user)],
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all users (admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    
    return [
        {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at,
            "daily_requests_count": user.daily_requests_count,
            "last_request_date": user.last_request_date
        }
        for user in users
    ]

@router.put("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    admin_user: Annotated[User, Depends(get_admin_user)],
    db: Session = Depends(get_db)
):
    """Toggle user active status"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = not user.is_active
    db.commit()
    
    return {
        "message": f"User {user.username} {'activated' if user.is_active else 'deactivated'}",
        "is_active": user.is_active
    }