from typing import List, Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
import uuid
from pathlib import Path
from PIL import Image
import io

from ...core.database import get_db
from ...core.config import settings
from ...models.user import User
from ...models.project import Project, ProductImage
from .auth import get_current_active_user

router = APIRouter()

# Pydantic models
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    product_category: Optional[str] = None
    target_audience: Optional[str] = None
    brand_guidelines: Optional[dict] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    product_category: Optional[str] = None
    target_audience: Optional[str] = None
    brand_guidelines: Optional[dict] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    product_category: Optional[str]
    target_audience: Optional[str]
    brand_guidelines: Optional[dict]
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True

class ProductImageResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    width: Optional[int]
    height: Optional[int]
    is_primary: bool
    uploaded_at: str
    
    class Config:
        from_attributes = True

class ProjectWithImagesResponse(ProjectResponse):
    product_images: List[ProductImageResponse] = []

def save_uploaded_file(file: UploadFile, project_id: int) -> tuple:
    """Save uploaded file and return file info"""
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1].lower()
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    # Create project directory
    project_dir = Path(settings.UPLOAD_DIR) / f"project_{project_id}"
    project_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = project_dir / unique_filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    # Get image dimensions
    width, height = None, None
    try:
        with Image.open(file_path) as img:
            width, height = img.size
    except Exception:
        pass
    
    return str(file_path), len(content), width, height

@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Create a new project"""
    
    db_project = Project(
        name=project.name,
        description=project.description,
        product_category=project.product_category,
        target_audience=project.target_audience,
        brand_guidelines=project.brand_guidelines,
        owner_id=current_user.id
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return db_project

@router.get("/", response_model=List[ProjectResponse])
def get_projects(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get user's projects"""
    
    projects = db.query(Project).filter(
        Project.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return projects

@router.get("/{project_id}", response_model=ProjectWithImagesResponse)
def get_project(
    project_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Get project by ID with images"""
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Update project"""
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update fields
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return project

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Delete project"""
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Delete associated files
    project_dir = Path(settings.UPLOAD_DIR) / f"project_{project_id}"
    if project_dir.exists():
        import shutil
        shutil.rmtree(project_dir)
    
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}

@router.post("/{project_id}/images", response_model=ProductImageResponse)
async def upload_product_image(
    project_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    is_primary: bool = Form(False)
):
    """Upload product image to project"""
    
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Validate file
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in settings.allowed_extensions_list:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed types: {', '.join(settings.allowed_extensions_list)}"
        )
    
    try:
        # Save file
        file_path, file_size, width, height = save_uploaded_file(file, project_id)
        
        # If this is set as primary, unset other primary images
        if is_primary:
            db.query(ProductImage).filter(
                ProductImage.project_id == project_id,
                ProductImage.is_primary == True
            ).update({"is_primary": False})
        
        # Create database record
        db_image = ProductImage(
            project_id=project_id,
            filename=Path(file_path).name,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type,
            width=width,
            height=height,
            is_primary=is_primary
        )
        
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        return db_image
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@router.get("/{project_id}/images", response_model=List[ProductImageResponse])
def get_project_images(
    project_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Get all images for a project"""
    
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    images = db.query(ProductImage).filter(
        ProductImage.project_id == project_id
    ).order_by(ProductImage.is_primary.desc(), ProductImage.uploaded_at.desc()).all()
    
    return images

@router.delete("/{project_id}/images/{image_id}")
def delete_product_image(
    project_id: int,
    image_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Delete product image"""
    
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get image
    image = db.query(ProductImage).filter(
        ProductImage.id == image_id,
        ProductImage.project_id == project_id
    ).first()
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Delete file
    try:
        if os.path.exists(image.file_path):
            os.remove(image.file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")
    
    # Delete database record
    db.delete(image)
    db.commit()
    
    return {"message": "Image deleted successfully"}

@router.put("/{project_id}/images/{image_id}/primary")
def set_primary_image(
    project_id: int,
    image_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Set image as primary for project"""
    
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get image
    image = db.query(ProductImage).filter(
        ProductImage.id == image_id,
        ProductImage.project_id == project_id
    ).first()
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Unset other primary images
    db.query(ProductImage).filter(
        ProductImage.project_id == project_id,
        ProductImage.is_primary == True
    ).update({"is_primary": False})
    
    # Set this image as primary
    image.is_primary = True
    db.commit()
    
    return {"message": "Primary image updated successfully"}