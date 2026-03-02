"""Add performance indexes for N+1 query optimization

Revision ID: 001_performance_indexes
Revises: 
Create Date: 2026-03-02 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_performance_indexes'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Add composite indexes for performance optimization"""
    
    # Post table indexes
    op.create_index(
        'idx_post_user_schedule',
        'posts',
        ['user_id', 'scheduled_time'],
        unique=False
    )
    op.create_index(
        'idx_post_user_platform_status',
        'posts',
        ['user_id', 'platform', 'status'],
        unique=False
    )
    op.create_index(
        'idx_post_scheduled_status',
        'posts',
        ['scheduled_time', 'status'],
        unique=False
    )
    
    # Translation table indexes
    op.create_index(
        'idx_translation_content_target',
        'translations',
        ['content_id', 'target_language'],
        unique=False
    )
    op.create_index(
        'idx_translation_languages',
        'translations',
        ['source_language', 'target_language'],
        unique=False
    )


def downgrade():
    """Remove performance indexes"""
    
    # Drop Post indexes
    op.drop_index('idx_post_user_schedule', table_name='posts')
    op.drop_index('idx_post_user_platform_status', table_name='posts')
    op.drop_index('idx_post_scheduled_status', table_name='posts')
    
    # Drop Translation indexes
    op.drop_index('idx_translation_content_target', table_name='translations')
    op.drop_index('idx_translation_languages', table_name='translations')
