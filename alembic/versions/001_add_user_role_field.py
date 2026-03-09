"""create users table with uuid pk and freelancer fields

Revision ID: 001_add_user_role_field
Revises:
Create Date: 2026-02-17 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = '001_add_user_role_field'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('password_hash', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('role', sa.String(), server_default='user', nullable=False),
        sa.Column('skills', sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column('experience_summary', sa.String(), nullable=True),
        sa.Column('portfolio_links', sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column('preferred_rate', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.UniqueConstraint('email', name='uq_users_email'),
        sa.UniqueConstraint('username', name='uq_users_username'),
    )
    op.create_index('ix_users_created_at', 'users', ['created_at'])
    op.create_index('ix_users_is_active', 'users', ['is_active'])

def downgrade():
    op.drop_table('users')