
import pytest
from ckan.tests.pytest_ckan.fixtures import clean_db, app, with_plugins

@pytest.fixture
def dashboard_plugin():
    return "dashboard"

@pytest.fixture
def with_dashboard_plugin(with_plugins):
    return with_plugins(["dashboard"])