import pytest


@pytest.fixture
def clean_db(reset_db, migrate_db_for):
    """Clean and initialize the database."""
    reset_db()
    migrate_db_for("dashboard")
