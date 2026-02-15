"""Change role column from enum to varchar

Revision ID: 002_change_role_varchar
Revises: 001_add_user_role
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_change_role_varchar'
down_revision = '001_add_user_role'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Change role column from enum to VARCHAR
    # First, alter the column type
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE VARCHAR USING role::text")
    
    # Drop the enum type if it exists (optional, can keep it for future use)
    # op.execute("DROP TYPE IF EXISTS userrole")


def downgrade() -> None:
    # Recreate enum type
    op.execute("CREATE TYPE userrole AS ENUM ('user', 'admin')")
    
    # Change column back to enum
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE userrole USING role::userrole")
