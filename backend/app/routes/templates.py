from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.config.database import get_db
from app.models import User
from app.models.template import Template, TemplateCategory
from app.auth.dependencies import get_current_user

router = APIRouter()

# Request/Response Schemas
class TemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: TemplateCategory
    content: str
    language: str = "english"
    tone: str = "professional"
    platform: Optional[str] = None
    is_public: bool = False

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[TemplateCategory] = None
    content: Optional[str] = None
    language: Optional[str] = None
    tone: Optional[str] = None
    platform: Optional[str] = None
    is_public: Optional[bool] = None
    is_favorite: Optional[bool] = None

class TemplateResponse(BaseModel):
    id: int
    user_id: Optional[int]
    name: str
    description: Optional[str]
    category: TemplateCategory
    content: str
    language: str
    tone: str
    platform: Optional[str]
    is_public: bool
    is_system: bool
    is_favorite: bool
    usage_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# System Templates (Pre-defined)
SYSTEM_TEMPLATES = [
    {
        "name": "Product Launch",
        "description": "Announce a new product launch",
        "category": TemplateCategory.PRODUCT,
        "content": "🚀 Exciting News! We're thrilled to announce the launch of [Product Name]!\n\n✨ [Key Feature 1]\n✨ [Key Feature 2]\n✨ [Key Feature 3]\n\nAvailable now at [Link]\n\n#ProductLaunch #Innovation",
        "language": "english",
        "tone": "exciting",
        "platform": "instagram"
    },
    {
        "name": "Event Invitation",
        "description": "Invite people to an event",
        "category": TemplateCategory.EVENT,
        "content": "📅 You're Invited!\n\nJoin us for [Event Name]\n📍 [Location]\n🕐 [Date & Time]\n\n[Brief Description]\n\nRSVP: [Link]\n\n#Event #Community",
        "language": "english",
        "tone": "friendly",
        "platform": "facebook"
    },
    {
        "name": "Blog Post Intro",
        "description": "Introduction for blog posts",
        "category": TemplateCategory.BLOG,
        "content": "In today's fast-paced world, [Topic] has become increasingly important. In this article, we'll explore [Key Points] and provide actionable insights to help you [Benefit].\n\nLet's dive in!",
        "language": "english",
        "tone": "professional",
        "platform": None
    },
    {
        "name": "Sale Announcement",
        "description": "Announce a sale or discount",
        "category": TemplateCategory.MARKETING,
        "content": "🎉 FLASH SALE ALERT! 🎉\n\nGet [Discount]% OFF on [Product/Category]\n\n⏰ Limited Time Only!\n🛍️ Shop Now: [Link]\n\nDon't miss out!\n\n#Sale #Discount #Shopping",
        "language": "english",
        "tone": "exciting",
        "platform": "twitter"
    },
    {
        "name": "Thank You Post",
        "description": "Thank your audience",
        "category": TemplateCategory.SOCIAL_MEDIA,
        "content": "🙏 Thank You!\n\nWe're incredibly grateful for your continued support. Your trust and loyalty mean the world to us.\n\nHere's to many more amazing moments together! ❤️\n\n#ThankYou #Gratitude #Community",
        "language": "english",
        "tone": "grateful",
        "platform": "instagram"
    },
    {
        "name": "Educational Tip",
        "description": "Share educational content",
        "category": TemplateCategory.EDUCATIONAL,
        "content": "💡 Did You Know?\n\n[Interesting Fact or Tip]\n\n[Brief Explanation]\n\nWant to learn more? [CTA]\n\n#Education #Learning #Tips",
        "language": "english",
        "tone": "informative",
        "platform": "linkedin"
    },
]


@router.post("/", response_model=TemplateResponse)
async def create_template(
    template: TemplateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new template.
    """
    new_template = Template(
        user_id=current_user.id,
        name=template.name,
        description=template.description,
        category=template.category,
        content=template.content,
        language=template.language,
        tone=template.tone,
        platform=template.platform,
        is_public=template.is_public,
        is_system=False
    )
    
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    
    return new_template


@router.get("/", response_model=List[TemplateResponse])
async def get_templates(
    current_user: User = Depends(get_current_user),
    category: Optional[TemplateCategory] = None,
    platform: Optional[str] = None,
    language: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all templates (user's + public + system).
    """
    query = db.query(Template).filter(
        (Template.user_id == current_user.id) | 
        (Template.is_public == True) | 
        (Template.is_system == True)
    )
    
    if category:
        query = query.filter(Template.category == category)
    if platform:
        query = query.filter(Template.platform == platform)
    if language:
        query = query.filter(Template.language == language)
    
    templates = query.order_by(Template.created_at.desc()).all()
    
    return templates


@router.get("/system", response_model=List[TemplateResponse])
async def get_system_templates(db: Session = Depends(get_db)):
    """
    Get all system templates.
    """
    templates = db.query(Template).filter(Template.is_system == True).all()
    
    # If no system templates exist, create them
    if not templates:
        for template_data in SYSTEM_TEMPLATES:
            template = Template(
                user_id=None,
                is_system=True,
                **template_data
            )
            db.add(template)
        
        db.commit()
        templates = db.query(Template).filter(Template.is_system == True).all()
    
    return templates


@router.get("/user", response_model=List[TemplateResponse])
async def get_user_templates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's own templates.
    """
    templates = db.query(Template).filter(Template.user_id == current_user.id).order_by(Template.created_at.desc()).all()
    
    return templates


@router.get("/favorites", response_model=List[TemplateResponse])
async def get_favorite_templates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's favorite templates.
    """
    templates = db.query(Template).filter(
        Template.user_id == current_user.id,
        Template.is_favorite == True
    ).order_by(Template.created_at.desc()).all()
    
    return templates


@router.get("/category/{category}", response_model=List[TemplateResponse])
async def get_templates_by_category(
    category: TemplateCategory,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get templates by category.
    """
    templates = db.query(Template).filter(
        Template.category == category,
        (Template.user_id == current_user.id) | (Template.is_public == True) | (Template.is_system == True)
    ).order_by(Template.created_at.desc()).all()
    
    return templates


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: int, db: Session = Depends(get_db)):
    """
    Get a specific template.
    """
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return template


@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: int,
    template_update: TemplateUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a template.
    """
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.user_id == current_user.id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Update fields
    if template_update.name is not None:
        template.name = template_update.name
    if template_update.description is not None:
        template.description = template_update.description
    if template_update.category is not None:
        template.category = template_update.category
    if template_update.content is not None:
        template.content = template_update.content
    if template_update.language is not None:
        template.language = template_update.language
    if template_update.tone is not None:
        template.tone = template_update.tone
    if template_update.platform is not None:
        template.platform = template_update.platform
    if template_update.is_public is not None:
        template.is_public = template_update.is_public
    if template_update.is_favorite is not None:
        template.is_favorite = template_update.is_favorite
    
    template.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(template)
    
    return template


@router.delete("/{template_id}")
async def delete_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a template.
    """
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.user_id == current_user.id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Can't delete system templates
    if template.is_system:
        raise HTTPException(status_code=400, detail="Cannot delete system templates")
    
    db.delete(template)
    db.commit()
    
    return {"status": "success", "message": "Template deleted successfully"}


@router.post("/{template_id}/use")
async def use_template(template_id: int, db: Session = Depends(get_db)):
    """
    Increment usage count when template is used.
    """
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template.usage_count += 1
    db.commit()
    
    return {"status": "success", "usage_count": template.usage_count}


@router.post("/{template_id}/favorite")
async def toggle_favorite(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle favorite status.
    """
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.user_id == current_user.id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template.is_favorite = not template.is_favorite
    db.commit()
    
    return {"status": "success", "is_favorite": template.is_favorite}


@router.get("/stats/popular", response_model=List[TemplateResponse])
async def get_popular_templates(limit: int = 10, db: Session = Depends(get_db)):
    """
    Get most popular templates by usage count.
    """
    templates = db.query(Template).filter(
        (Template.is_public == True) | (Template.is_system == True)
    ).order_by(Template.usage_count.desc()).limit(limit).all()
    
    return templates
