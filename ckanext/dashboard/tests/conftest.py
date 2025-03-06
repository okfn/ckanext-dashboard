
import pytest
import ckan.tests.factories as factories
import ckan.model as model
from flask import Flask


@pytest.fixture
def clean_db():
    """Clean and initialize the database."""
    model.repo.clean_db()
    model.repo.rebuild_db()


@pytest.fixture
def sysadmin_user():
    """Return a sysadmin user."""
    return factories.Sysadmin()


@pytest.fixture
def normal_user():
    """Return a normal (non-sysadmin) user."""
    return factories.User()


@pytest.fixture
def test_dataset():
    """Create a test dataset."""
    user = factories.User()
    org = factories.Organization(user=user)
    return factories.Dataset(user=user, owner_org=org["id"])


@pytest.fixture
def test_resource(test_dataset):
    """Create a test resource."""
    return factories.Resource(package_id=test_dataset["id"])


@pytest.fixture
def app():
    """Return a WSGI app for testing Flask routes directly."""
    # For integration tests, we use a mock app
    flask_app = Flask('test_app')
    # Return the Flask app directly so it can be used in app.app_context()
    return flask_app

@pytest.fixture
def create_test_data(clean_db):
    """Create some default test data for CKAN."""
    # Create a sysadmin user, an organization, a dataset, and a resource.
    sysadmin = factories.Sysadmin()
    user = factories.User()
    org = factories.Organization(user=user)
    dataset = factories.Dataset(user=user, owner_org=org["id"])
    resource = factories.Resource(package_id=dataset["id"])
    return {
        'sysadmin': sysadmin,
        'user': user,
        'organization': org,
        'dataset': dataset,
        'resource': resource
    }
