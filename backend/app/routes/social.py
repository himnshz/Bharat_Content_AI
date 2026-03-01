from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.config.database import get_db
from app.models import Post, Platform, PostStatus, Content, User

router = APIRouter()

# Request/Response Schemas
class PostScheduleRequest(BaseModel):
    user_id: int = Field(..., description="User ID")
    content_id: Optional[int] = Field(None, description="Content ID to post (optional)")
    text_content: str = Field(..., min_length=1, max_length=10000, description="Post text content")
    platform: Platform = Field(..., description="Social media platform")
    scheduled_time: datetime = Field(..., description="When to publish the post")
    media_urls: Optional[List[str]] = Field(default=None, description="List of media URLs")
    title: Optional[str] = Field(None, max_length=500, description="Post title")

class PostUpdateRequest(BaseModel):
    text_content: Optional[str] = Field(None, description="Updated post text")
    scheduled_time: Optional[datetime] = Field(None, description="Updated schedule time")
    status: Optional[PostStatus] = Field(None, description="Updated post status")

class PostResponse(BaseModel):
    id: int
    user_id: int
    content_id: Optional[int]
    title: Optional[str]
    text_content: str
    platform: Platform
    status: PostStatus
    scheduled_time: Optional[datetime]
    published_time: Optional[datetime]
    media_urls: Optional[List[str]]
    likes_count: int
    comments_count: int
    shares_count: int
    views_count: int
    engagement_rate: int
    platform_post_id: Optional[str]
    platform_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostListResponse(BaseModel):
    total: int
    items: List[PostResponse]

class BulkScheduleRequest(BaseModel):
    user_id: int
    content_id: int
    platforms: List[Platform] = Field(..., min_items=1, description="List of platforms to post to")
    scheduled_time: datetime
    customize_per_platform: bool = Field(default=False, description="Whether to customize content per platform")


@router.post("/schedule", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def schedule_post(request: PostScheduleRequest, db: Session = Depends(get_db)):
    """
    Schedule a post to a social media platform.
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify content exists if content_id provided
        if request.content_id:
            content = db.query(Content).filter(Content.id == request.content_id).first()
            if not content:
                raise HTTPException(status_code=404, detail="Content not found")
        
        # Validate scheduled time is in the future
        if request.scheduled_time <= datetime.utcnow():
            raise HTTPException(status_code=400, detail="Scheduled time must be in the future")
        
        # Create post record
        post = Post(
            user_id=request.user_id,
            content_id=request.content_id,
            title=request.title,
            text_content=request.text_content,
            platform=request.platform,
            status=PostStatus.SCHEDULED,
            scheduled_time=request.scheduled_time,
            media_urls=request.media_urls
        )
        
        db.add(post)
        db.commit()
        db.refresh(post)
        
        # Update user stats
        user.posts_scheduled_count += 1
        db.commit()
        
        # TODO: Integrate with AWS EventBridge or background task scheduler
        # schedule_post_task(post.id, request.scheduled_time)
        
        return post
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to schedule post: {str(e)}")


@router.post("/schedule/bulk", response_model=List[PostResponse], status_code=status.HTTP_201_CREATED)
async def bulk_schedule_posts(request: BulkScheduleRequest, db: Session = Depends(get_db)):
    """
    Schedule the same content to multiple platforms at once.
    """
    try:
        # Verify user and content
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        content = db.query(Content).filter(Content.id == request.content_id).first()
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        # Validate scheduled time
        if request.scheduled_time <= datetime.utcnow():
            raise HTTPException(status_code=400, detail="Scheduled time must be in the future")
        
        posts = []
        for platform in request.platforms:
            # Customize content per platform if needed
            text_content = content.edited_content or content.generated_content
            
            if request.customize_per_platform:
                # Platform-specific customization logic
                if platform == Platform.TWITTER:
                    text_content = text_content[:280]  # Twitter character limit
                elif platform == Platform.LINKEDIN:
                    text_content = f"{text_content}\n\n#Professional #Business"
            
            post = Post(
                user_id=request.user_id,
                content_id=request.content_id,
                text_content=text_content,
                platform=platform,
                status=PostStatus.SCHEDULED,
                scheduled_time=request.scheduled_time
            )
            
            db.add(post)
            posts.append(post)
        
        db.commit()
        
        # Refresh all posts
        for post in posts:
            db.refresh(post)
        
        # Update user stats
        user.posts_scheduled_count += len(posts)
        db.commit()
        
        return posts
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Bulk scheduling failed: {str(e)}")


@router.get("/list", response_model=PostListResponse)
async def list_posts(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    platform: Optional[Platform] = None,
    status: Optional[PostStatus] = None,
    db: Session = Depends(get_db)
):
    """
    List all posts for a user with optional filters.
    """
    query = db.query(Post).filter(Post.user_id == user_id)
    
    if platform:
        query = query.filter(Post.platform == platform)
    if status:
        query = query.filter(Post.status == status)
    
    total = query.count()
    items = query.order_by(Post.scheduled_time.desc()).offset(skip).limit(limit).all()
    
    return PostListResponse(total=total, items=items)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Get a specific post by ID.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, request: PostUpdateRequest, db: Session = Depends(get_db)):
    """
    Update a scheduled post.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Only allow updates for draft or scheduled posts
    if post.status not in [PostStatus.DRAFT, PostStatus.SCHEDULED]:
        raise HTTPException(status_code=400, detail="Cannot update published or failed posts")
    
    if request.text_content:
        post.text_content = request.text_content
    if request.scheduled_time:
        if request.scheduled_time <= datetime.utcnow():
            raise HTTPException(status_code=400, detail="Scheduled time must be in the future")
        post.scheduled_time = request.scheduled_time
    if request.status:
        post.status = request.status
    
    post.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(post)
    
    return post


@router.post("/{post_id}/publish", response_model=PostResponse)
async def publish_post_now(post_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Publish a post immediately (bypass scheduling).
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.status == PostStatus.PUBLISHED:
        raise HTTPException(status_code=400, detail="Post already published")
    
    try:
        post.status = PostStatus.PUBLISHING
        db.commit()
        
        # TODO: Integrate with actual social media APIs
        # background_tasks.add_task(publish_to_platform, post.id, post.platform)
        
        # Mock successful publish
        post.status = PostStatus.PUBLISHED
        post.published_time = datetime.utcnow()
        post.platform_post_id = f"mock_{post.platform.value}_{post.id}"
        post.platform_url = f"https://{post.platform.value}.com/post/{post.id}"
        
        db.commit()
        db.refresh(post)
        
        return post
        
    except Exception as e:
        post.status = PostStatus.FAILED
        post.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Failed to publish post: {str(e)}")


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Delete a post (only if not published).
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.status == PostStatus.PUBLISHED:
        raise HTTPException(status_code=400, detail="Cannot delete published posts")
    
    db.delete(post)
    db.commit()
    
    return None


@router.post("/{post_id}/cancel", response_model=PostResponse)
async def cancel_scheduled_post(post_id: int, db: Session = Depends(get_db)):
    """
    Cancel a scheduled post.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.status != PostStatus.SCHEDULED:
        raise HTTPException(status_code=400, detail="Only scheduled posts can be cancelled")
    
    post.status = PostStatus.CANCELLED
    post.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(post)
    
    return post


@router.get("/calendar/{user_id}")
async def get_post_calendar(
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    """
    Get all scheduled posts for a user within a date range (for calendar view).
    """
    posts = db.query(Post).filter(
        Post.user_id == user_id,
        Post.scheduled_time >= start_date,
        Post.scheduled_time <= end_date,
        Post.status.in_([PostStatus.SCHEDULED, PostStatus.PUBLISHED])
    ).order_by(Post.scheduled_time).all()
    
    # Group by date for calendar display
    calendar_data = {}
    for post in posts:
        date_key = post.scheduled_time.date().isoformat()
        if date_key not in calendar_data:
            calendar_data[date_key] = []
        calendar_data[date_key].append({
            "id": post.id,
            "platform": post.platform.value,
            "status": post.status.value,
            "time": post.scheduled_time.isoformat(),
            "title": post.title or post.text_content[:50]
        })
    
    return {"calendar": calendar_data, "total_posts": len(posts)}
