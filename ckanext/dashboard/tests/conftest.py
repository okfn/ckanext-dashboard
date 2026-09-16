import contextlib

import pytest
from ckan import model
from ckan.plugins import toolkit


@pytest.fixture
def clean_db(reset_db, migrate_db_for):
    """Clean and initialize the database."""
    reset_db()
    if toolkit.check_ckan_version(min_version="2.11"):
        migrate_db_for("dashboard")
    else:
        migrate_old()


def migrate_old():
    """Apply extension migrations using the CKAN 2.10 repository API."""
    from ckan.cli.db import _resolve_alembic_config

    @contextlib.contextmanager
    def _repo_for_plugin(plugin):
        original = model.repo._alembic_ini
        model.repo._alembic_ini = _resolve_alembic_config(plugin)
        try:
            yield model.repo
        finally:
            model.repo._alembic_ini = original

    with _repo_for_plugin("dashboard") as repo:
        repo.upgrade_db("head")
