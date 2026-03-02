from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.config.database import get_db
from app.models.campaign import Campaign, CampaignStatus, CampaignType
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter(tags=["Campaigns"])

# Pydantic schemas for request/response

class CampaignBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    campaign_type: CampaignType = CampaignType.AWARENESS
    status: CampaignStatus = CampaignStatus.DRAFT
    objectives: Optional[List[str]] = []
    target_audience: Optional[dict] = {}
    budget: Optional[float] = None
    currency: str = "USD"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    platforms: Optional[List[str]] = []
    content_guidelines: Optional[str] = None
    hashtags: Optional[List[str]] = []
    mentions: Optional[List[str]] = []
    creator_ids: Optional[List[int]] = []
    min_followers: Optional[int] = None
    max_creators: Optional[int] = None
    target_reach: Optional[int] = None
    target_impressions: Optional[int] = None
    target_engagement_rate: Optional[float] = None
    target_conversions: Optional[int] = None
    requires_approval: bool = True
    brand_assets: Optional[List[str]] = []
    landing_page_url: Optional[str] = None
    tracking_links: Optional[List[str]] = []
    team_members: Optional[List[int]] = []
    notes: Optional[str] = None

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    campaign_type: Optional[CampaignType] = None
    status: Optional[CampaignStatus] = None
    objectives: Optional[List[str]] = None
    target_audience: Optional[dict] = None
    budget: Optional[float] = None
    currency: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    platforms: Optional[List[str]] = None
    content_guidelines: Optional[str] = None
    hashtags: Optional[List[str]] = None
    mentions: Optional[List[str]] = None
    creator_ids: Optional[List[int]] = None
    min_followers: Optional[int] = None
    max_creators: Optional[int] = None
    target_reach: Optional[int] = None
    target_impressions: Optional[int] = None
    target_engagement_rate: Optional[float] = None
    target_conversions: Optional[int] = None
    requires_approval: Optional[bool] = None
    brand_assets: Optional[List[str]] = None
    landing_page_url: Optional[str] = None
    tracking_links: Optional[List[str]] = None
    team_members: Optional[List[int]] = None
    notes: Optional[str] = None

class CampaignMetricsUpdate(BaseModel):
    actual_reach: Optional[int] = None
    actual_impressions: Optional[int] = None
    actual_engagement_rate: Optional[float] = None
    actual_conversions: Optional[int] = None
    total_spent: Optional[float] = None
    revenue_generated: Optional[float] = None

class CampaignResponse(CampaignBase):
    id: int
    user_id: int
    actual_reach: int
    actual_impressions: int
    actual_engagement_rate: float
    actual_conversions: int
    total_spent: float
    revenue_generated: float
    roi: float
    approved_by: Optional[int]
    approved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    is_active: bool
    days_remaining: Optional[int]
    budget_spent_percentage: float

    class Config:
        from_attributes = True


# CRUD Endpoints

@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new campaign
    
    - **name**: Campaign name (required)
    - **description**: Campaign description
    - **campaign_type**: Type of campaign (influencer, brand, product_launch, etc.)
    - **status**: Campaign status (draft, active, paused, completed, cancelled)
    - **budget**: Total campaign budget
    - **start_date**: Campaign start date
    - **end_date**: Campaign end date
    - **platforms**: List of target platforms
    - **target_audience**: Demographics and targeting info
    """
    try:
        # Create campaign instance with authenticated user
        campaign = Campaign(**campaign_data.model_dump(), user_id=current_user.id)
        
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        
        return campaign
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create campaign: {str(e)}"
        )


@router.get("/", response_model=List[CampaignResponse])
async def get_campaigns(
    status: Optional[CampaignStatus] = Query(None, description="Filter by status"),
    campaign_type: Optional[CampaignType] = Query(None, description="Filter by type"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all campaigns for authenticated user with optional filters
    
    - **status**: Filter by campaign status
    - **campaign_type**: Filter by campaign type
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    try:
        query = db.query(Campaign).filter(Campaign.user_id == current_user.id)
        
        if status:
            query = query.filter(Campaign.status == status)
        if campaign_type:
            query = query.filter(Campaign.campaign_type == campaign_type)
        
        campaigns = query.order_by(Campaign.created_at.desc()).offset(skip).limit(limit).all()
        return campaigns
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch campaigns: {str(e)}"
        )


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific campaign by ID
    
    - **campaign_id**: The ID of the campaign to retrieve
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    return campaign


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: int,
    campaign_data: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing campaign
    
    - **campaign_id**: The ID of the campaign to update
    - All fields are optional - only provided fields will be updated
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    try:
        # Update only provided fields
        update_data = campaign_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(campaign, field, value)
        
        campaign.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(campaign)
        
        return campaign
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update campaign: {str(e)}"
        )


@router.patch("/{campaign_id}/metrics", response_model=CampaignResponse)
async def update_campaign_metrics(
    campaign_id: int,
    metrics: CampaignMetricsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update campaign performance metrics
    
    - **campaign_id**: The ID of the campaign
    - **actual_reach**: Actual reach achieved
    - **actual_impressions**: Actual impressions
    - **actual_engagement_rate**: Actual engagement rate
    - **actual_conversions**: Actual conversions
    - **total_spent**: Total amount spent
    - **revenue_generated**: Revenue generated from campaign
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    try:
        # Update metrics
        update_data = metrics.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(campaign, field, value)
        
        # Calculate ROI if both spent and revenue are available
        if campaign.total_spent and campaign.total_spent > 0:
            campaign.roi = ((campaign.revenue_generated - campaign.total_spent) / campaign.total_spent) * 100
        
        campaign.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(campaign)
        
        return campaign
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update campaign metrics: {str(e)}"
        )


@router.patch("/{campaign_id}/status", response_model=CampaignResponse)
async def update_campaign_status(
    campaign_id: int,
    new_status: CampaignStatus,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update campaign status
    
    - **campaign_id**: The ID of the campaign
    - **new_status**: New status (draft, active, paused, completed, cancelled)
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    try:
        campaign.status = new_status
        campaign.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(campaign)
        
        return campaign
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update campaign status: {str(e)}"
        )


@router.patch("/{campaign_id}/approve")
async def approve_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Approve a campaign (user approves their own campaign or team member approves)
    
    - **campaign_id**: The ID of the campaign to approve
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    try:
        campaign.approved_by = current_user.id
        campaign.approved_at = datetime.utcnow()
        campaign.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(campaign)
        
        return {
            "message": "Campaign approved successfully",
            "campaign_id": campaign_id,
            "approved_by": current_user.id,
            "approved_at": campaign.approved_at
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to approve campaign: {str(e)}"
        )


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a campaign
    
    - **campaign_id**: The ID of the campaign to delete
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    try:
        db.delete(campaign)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete campaign: {str(e)}"
        )


@router.get("/{campaign_id}/analytics")
async def get_campaign_analytics(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed analytics for a campaign
    
    - **campaign_id**: The ID of the campaign
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Calculate performance metrics
    reach_percentage = (campaign.actual_reach / campaign.target_reach * 100) if campaign.target_reach else 0
    impressions_percentage = (campaign.actual_impressions / campaign.target_impressions * 100) if campaign.target_impressions else 0
    engagement_percentage = (campaign.actual_engagement_rate / campaign.target_engagement_rate * 100) if campaign.target_engagement_rate else 0
    conversions_percentage = (campaign.actual_conversions / campaign.target_conversions * 100) if campaign.target_conversions else 0
    
    return {
        "campaign_id": campaign.id,
        "campaign_name": campaign.name,
        "status": campaign.status,
        "is_active": campaign.is_active,
        "days_remaining": campaign.days_remaining,
        "budget": {
            "total": campaign.budget,
            "spent": campaign.total_spent,
            "remaining": campaign.budget - campaign.total_spent if campaign.budget else None,
            "spent_percentage": campaign.budget_spent_percentage
        },
        "performance": {
            "reach": {
                "target": campaign.target_reach,
                "actual": campaign.actual_reach,
                "percentage": round(reach_percentage, 2)
            },
            "impressions": {
                "target": campaign.target_impressions,
                "actual": campaign.actual_impressions,
                "percentage": round(impressions_percentage, 2)
            },
            "engagement_rate": {
                "target": campaign.target_engagement_rate,
                "actual": campaign.actual_engagement_rate,
                "percentage": round(engagement_percentage, 2)
            },
            "conversions": {
                "target": campaign.target_conversions,
                "actual": campaign.actual_conversions,
                "percentage": round(conversions_percentage, 2)
            }
        },
        "roi": {
            "total_spent": campaign.total_spent,
            "revenue_generated": campaign.revenue_generated,
            "roi_percentage": round(campaign.roi, 2),
            "profit": campaign.revenue_generated - campaign.total_spent
        },
        "timeline": {
            "start_date": campaign.start_date,
            "end_date": campaign.end_date,
            "created_at": campaign.created_at,
            "updated_at": campaign.updated_at
        }
    }
