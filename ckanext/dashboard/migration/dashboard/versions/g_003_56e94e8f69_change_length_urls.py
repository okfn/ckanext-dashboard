"""Add secondary button fields

Revision ID: f156e94e8f68
Revises: f156e94e8f68
Create Date: 2025-08-07 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f156e94e8f68'
down_revision = 'f156e94e8f68'
branch_labels = None
depends_on = None


def upgrade():
    # Add secondary_button_url column
    op.add_column(
        'dashboard_dashboard',
        sa.Column('secondary_button_url', sa.String(length=2000), nullable=True)
    )

    # Add secondary_button_title column
    op.add_column(
        'dashboard_dashboard',
        sa.Column('secondary_button_title', sa.String(length=200), nullable=True)
    )


def downgrade():
    # Remove secondary_button_title column
    op.drop_column('dashboard_dashboard', 'secondary_button_title')

    # Remove secondary_button_url column
    op.drop_column('dashboard_dashboard', 'secondary_button_url')
