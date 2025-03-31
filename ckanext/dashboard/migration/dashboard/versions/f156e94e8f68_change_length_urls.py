"""Change Length URLs

Revision ID: f156e94e8f68
Revises: 43a02b9d1c09
Create Date: 2025-03-31 12:59:29.474776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f156e94e8f68'
down_revision = '43a02b9d1c09'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('dashboard_dashboard', 'embeded_url',
                    existing_type=sa.String(length=200),
                    type_=sa.String(length=2000),
                    existing_nullable=True)

    op.alter_column('dashboard_dashboard', 'report_url',
                    existing_type=sa.String(length=200),
                    type_=sa.String(length=2000),
                    existing_nullable=True)


def downgrade():
    op.alter_column('dashboard_dashboard', 'embeded_url',
                    existing_type=sa.String(length=2000),
                    type_=sa.String(length=200),
                    existing_nullable=True)

    op.alter_column('dashboard_dashboard', 'report_url',
                    existing_type=sa.String(length=2000),
                    type_=sa.String(length=200),
                    existing_nullable=True)
