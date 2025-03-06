import pytest
import ckan.tests.factories as factories
import ckan.model as model
from ckan.tests.helpers import _get_test_app
from ckanext.dashboard.models import DatasetDashboard


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
    return _get_test_app()


@pytest.fixture
def initialize_dashboard_db():
    """Create the dashboard table in the database."""
    engine = model.meta.engine
    DatasetDashboard.__table__.create(engine, checkfirst=True)
    yield
    DatasetDashboard.__table__.drop(engine, checkfirst=True)


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


@pytest.fixture
def dashboard_test_data(clean_db, initialize_dashboard_db):
    """Create test data specifically for dashboard tests."""
    sysadmin = factories.Sysadmin()
    sysadmin["headers"] = {"Authorization": sysadmin["apikey"]}

    user = factories.User()
    user["headers"] = {"Authorization": user["apikey"]}

    org = factories.Organization(user=user)
    dataset = factories.Dataset(user=user, owner_org=org["id"])

    class TestData:
        def __init__(self):
            self.sysadmin = sysadmin
            self.user = user
            self.organization = org
            self.dataset = dataset

    return TestData()


@pytest.fixture
def dashboard_entry(clean_db, initialize_dashboard_db, dashboard_test_data):
    """
    Crea un dashboard para el dataset de prueba y lo devuelve.
    Este dashboard se puede utilizar en los tests de actualización y eliminación.
    """
    from ckanext.dashboard.models import DatasetDashboard
    dashboard = DatasetDashboard(
        package_id=dashboard_test_data.dataset["id"],
        dashboard_type="tableau",
        embeded_url="https://example.com/dashboard/embed?id=12345",
        report_url="https://example.com/dashboard/report?id=12345"
    )
    model.Session.add(dashboard)
    model.Session.commit()
    yield dashboard
    # Limpieza: se elimina el dashboard creado
    model.Session.delete(dashboard)
    model.Session.commit()
