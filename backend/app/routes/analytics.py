from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta, date

from app.config.database import get_db
from app.models import (
    Analytics, ContentPerformance, Post, Content, User,
    Platform, ContentType, PostStatus
)

router = APIRouter()

# Response Schemas
class AnalyticsOverviewResponse(BaseModel):
    total_content_generated: int
    total_translations: int
    total_posts_scheduled: int
    total_posts_published: int
    total_engagement: Dict[str, int]
    avg_engagement_rate: float
    top_performing_language: Optional[str]
    top_performing_platform: Optional[Platform]
    period_start: date
    period_end: date

class PlatformPerformanceResponse(BaseModel):
    platform: Platform
    total_posts: int
    total_likes: int
    total_comments: int
    total_shares: int
    total_views: int
    avg_engagement_rate: float

class ContentTypePerformanceResponse(BaseModel):
    content_type: ContentType
    total_generated: int
    avg_word_count: float
    avg_quality_score: float
    most_used_language: str

class EngagementTrendResponse(BaseModel):
    date: date
    likes: int
    comments: int
    shares: int
    views: int
    engagement_rate: float

class TopPerformingContentResponse(BaseModel):
    content_id: int
    post_id: Optional[int]
    text_preview: str
    platform: Optional[Platform]
    language: str
    total_engagement: int
    engagement_rate: float
    published_at: Optional[datetime]


@router.get("/overview/{user_id}", response_model=AnalyticsOverviewResponse)
async def get_analytics_overview(
    user_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive analytics overview for a user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    
    # Content generation stats
    content_count = db.query(func.count(Content.id)).filter(
        Content.user_id == user_id,
        Content.created_at >= start_date
    ).scalar()
    
    # Post stats
    posts_scheduled = db.query(func.count(Post.id)).filter(
        Post.user_id == user_id,
        Post.status == PostStatus.SCHEDULED,
        Post.created_at >= start_date
    ).scalar()
    
    posts_published = db.query(func.count(Post.id)).filter(
        Post.user_id == user_id,
        Post.status == PostStatus.PUBLISHED,
        Post.published_time >= start_date
    ).scalar()
    
    # Engagement metrics
    engagement_stats = db.query(
        func.sum(Post.likes_count).label('total_likes'),
        func.sum(Post.comments_count).label('total_comments'),
        func.sum(Post.shares_count).label('total_shares'),
        func.sum(Post.views_count).label('total_views'),
        func.avg(Post.engagement_rate).label('avg_engagement_rate')
    ).filter(
        Post.user_id == user_id,
        Post.status == PostStatus.PUBLISHED,
        Post.published_time >= start_date
    ).first()
    
    # Top performing language
    top_language = db.query(
        Content.language,
        func.count(Content.id).label('count')
    ).filter(
        Content.user_id == user_id,
        Content.created_at >= start_date
    ).group_by(Content.language).order_by(desc('count')).first()
    
    # Top performing platform
    top_platform = db.query(
        Post.platform,
        func.sum(Post.likes_count + Post.comments_count + Post.shares_count).label('total_engagement')
    ).filter(
        Post.user_id == user_id,
        Post.status == PostStatus.PUBLISHED,
        Post.published_time >= start_date
    ).group_by(Post.platform).order_by(desc('total_engagement')).first()
    
    return AnalyticsOverviewResponse(
        total_content_generated=content_count or 0,
        total_translations=user.translations_count,
        total_posts_scheduled=posts_scheduled or 0,
        total_posts_published=posts_published or 0,
        total_engagement={
            "likes": engagement_stats.total_likes or 0,
            "comments": engagement_stats.total_comments or 0,
            "shares": engagement_stats.total_shares or 0,
            "views": engagement_stats.total_views or 0
        },
        avg_engagement_rate=float(engagement_stats.avg_engagement_rate or 0),
        top_performing_language=top_language[0] if top_language else None,
        top_performing_platform=top_platform[0] if top_platform else None,
        period_start=start_date,
        period_end=end_date
    )


@router.get("/platform-performance/{user_id}", response_model=List[PlatformPerformanceResponse])
async def get_platform_performance(
    user_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get performance metrics broken down by platform.
    """
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    platform_stats = db.query(
        Post.platform,
        func.count(Post.id).label('total_posts'),
        func.sum(Post.likes_count).label('total_likes'),
        func.sum(Post.comments_count).label('total_comments'),
        func.sum(Post.shares_count).label('total_shares'),
        func.sum(Post.views_count).label('total_views'),
        func.avg(Post.engagement_rate).label('avg_engagement_rate')
    ).filter(
        Post.user_id == user_id,
        Post.status == PostStatus.PUBLISHED,
        Post.published_time >= start_date
    ).group_by(Post.platform).all()
    
    results = []
    for stat in platform_stats:
        results.append(PlatformPerformanceResponse(
            platform=stat.platform,
            total_posts=stat.total_posts or 0,
            total_likes=stat.total_likes or 0,
            total_comments=stat.total_comments or 0,
            total_shares=stat.total_shares or 0,
            total_views=stat.total_views or 0,
            avg_engagement_rate=float(stat.avg_engagement_rate or 0)
        ))
    
    return results


@router.get("/content-type-performance/{user_id}", response_model=List[ContentTypePerformanceResponse])
async def get_content_type_performance(
    user_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get performance metrics broken down by content type.
    """
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    content_stats = db.query(
        Content.content_type,
        func.count(Content.id).label('total_generated'),
        func.avg(Content.word_count).label('avg_word_count'),
        func.avg(Content.quality_score).label('avg_quality_score'),
        Content.language
    ).filter(
        Content.user_id == user_id,
        Content.created_at >= start_date
    ).group_by(Content.content_type, Content.language).all()
    
    # Aggregate by content type (get most used language per type)
    type_aggregates = {}
    for stat in content_stats:
        if stat.content_type not in type_aggregates:
            type_aggregates[stat.content_type] = {
                'total': 0,
                'word_count_sum': 0,
                'quality_sum': 0,
                'languages': {}
            }
        
        type_aggregates[stat.content_type]['total'] += stat.total_generated
        type_aggregates[stat.content_type]['word_count_sum'] += (stat.avg_word_count or 0) * stat.total_generated
        type_aggregates[stat.content_type]['quality_sum'] += (stat.avg_quality_score or 0) * stat.total_generated
        type_aggregates[stat.content_type]['languages'][stat.language] = stat.total_generated
    
    results = []
    for content_type, data in type_aggregates.items():
        most_used_lang = max(data['languages'].items(), key=lambda x: x[1])[0] if data['languages'] else 'unknown'
        results.append(ContentTypePerformanceResponse(
            content_type=content_type,
            total_generated=data['total'],
            avg_word_count=data['word_count_sum'] / data['total'] if data['total'] > 0 else 0,
            avg_quality_score=data['quality_sum'] / data['total'] if data['total'] > 0 else 0,
            most_used_language=most_used_lang
        ))
    
    return results


@router.get("/engagement-trends/{user_id}", response_model=List[EngagementTrendResponse])
async def get_engagement_trends(
    user_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get daily engagement trends over time.
    """
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    # Query daily aggregates
    daily_stats = db.query(
        func.date(Post.published_time).label('date'),
        func.sum(Post.likes_count).label('likes'),
        func.sum(Post.comments_count).label('comments'),
        func.sum(Post.shares_count).label('shares'),
        func.sum(Post.views_count).label('views'),
        func.avg(Post.engagement_rate).label('engagement_rate')
    ).filter(
        Post.user_id == user_id,
        Post.status == PostStatus.PUBLISHED,
        Post.published_time >= start_date
    ).group_by(func.date(Post.published_time)).order_by('date').all()
    
    results = []
    for stat in daily_stats:
        results.append(EngagementTrendResponse(
            date=stat.date,
            likes=stat.likes or 0,
            comments=stat.comments or 0,
            shares=stat.shares or 0,
            views=stat.views or 0,
            engagement_rate=float(stat.engagement_rate or 0)
        ))
    
    return results


@router.get("/top-content/{user_id}", response_model=List[TopPerformingContentResponse])
async def get_top_performing_content(
    user_id: int,
    limit: int = 10,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get top performing content pieces based on engagement.
    """
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    # Join Content and Post to get engagement metrics
    top_content = db.query(
        Content.id.label('content_id'),
        Post.id.label('post_id'),
        Content.generated_content,
        Post.platform,
        Content.language,
        (Post.likes_count + Post.comments_count + Post.shares_count).label('total_engagement'),
        Post.engagement_rate,
        Post.published_time
    ).join(
        Post, Content.id == Post.content_id
    ).filter(
        Content.user_id == user_id,
        Post.status == PostStatus.PUBLISHED,
        Post.published_time >= start_date
    ).order_by(desc('total_engagement')).limit(limit).all()
    
    results = []
    for item in top_content:
        text_preview = item.generated_content[:100] + "..." if len(item.generated_content) > 100 else item.generated_content
        results.append(TopPerformingContentResponse(
            content_id=item.content_id,
            post_id=item.post_id,
            text_preview=text_preview,
            platform=item.platform,
            language=item.language,
            total_engagement=item.total_engagement,
            engagement_rate=float(item.engagement_rate or 0),
            published_at=item.published_time
        ))
    
    return results


@router.get("/language-distribution/{user_id}")
async def get_language_distribution(
    user_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get distribution of content across different languages.
    """
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    language_stats = db.query(
        Content.language,
        func.count(Content.id).label('count')
    ).filter(
        Content.user_id == user_id,
        Content.created_at >= start_date
    ).group_by(Content.language).all()
    
    total = sum(stat.count for stat in language_stats)
    
    distribution = {}
    for stat in language_stats:
        distribution[stat.language] = {
            "count": stat.count,
            "percentage": round((stat.count / total * 100), 2) if total > 0 else 0
        }
    
    return {
        "total_content": total,
        "languages": distribution
    }


@router.post("/sync-metrics/{post_id}")
async def sync_post_metrics(post_id: int, db: Session = Depends(get_db)):
    """
    Manually trigger sync of engagement metrics from social platform.
    This would typically be called by a background job.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.status != PostStatus.PUBLISHED:
        raise HTTPException(status_code=400, detail="Can only sync metrics for published posts")
    
    try:
        # TODO: Integrate with actual social media APIs to fetch real metrics
        # For now, simulate metric updates
        import random
        
        post.likes_count += random.randint(0, 50)
        post.comments_count += random.randint(0, 10)
        post.shares_count += random.randint(0, 20)
        post.views_count += random.randint(0, 500)
        
        # Calculate engagement rate
        if post.views_count > 0:
            total_engagement = post.likes_count + post.comments_count + post.shares_count
            post.engagement_rate = int((total_engagement / post.views_count) * 100)
        
        post.last_synced_at = datetime.utcnow()
        
        db.commit()
        db.refresh(post)
        
        return {
            "status": "success",
            "post_id": post.id,
            "metrics": {
                "likes": post.likes_count,
                "comments": post.comments_count,
                "shares": post.shares_count,
                "views": post.views_count,
                "engagement_rate": post.engagement_rate
            },
            "last_synced": post.last_synced_at
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to sync metrics: {str(e)}")
