"""Store package_id as text, matching CKAN package identifiers.

Revision ID: f156e94e8f70
Revises: f156e94e8f69
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'f156e94e8f70'
down_revision = 'f156e94e8f69'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'dashboard_dashboard', 'package_id',
        existing_type=postgresql.UUID(as_uuid=True),
        type_=sa.UnicodeText(),
        existing_nullable=False,
        postgresql_using='package_id::text',
    )


def downgrade():
    # Non-UUID identifiers must be resolved before reverting to the old schema.
    op.alter_column(
        'dashboard_dashboard', 'package_id',
        existing_type=sa.UnicodeText(),
        type_=postgresql.UUID(as_uuid=True),
        existing_nullable=False,
        postgresql_using='package_id::uuid',
    )
