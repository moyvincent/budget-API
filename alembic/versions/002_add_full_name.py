"""add full_name to users

Revision ID: 002
Revises: 001
Create Date: 2024-03-20 23:05:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add full_name column to users table
    op.add_column('users', sa.Column('full_name', sa.String(), nullable=True))

def downgrade() -> None:
    # Remove full_name column from users table
    op.drop_column('users', 'full_name') 