"""Create dashboard_package table

Revision ID: 43a02b9d1c09
Revises: 
Create Date: 2025-02-24 17:29:28.632072

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '43a02b9d1c09'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'dashboard_package',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('package_id', sa.String(36), nullable=False, unique=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.String(500)),
        sa.Column('embeded_url', sa.String(200)),
        sa.Column('report_url', sa.String(200))
    )


def downgrade():
    op.drop_table('dashboard_package')
