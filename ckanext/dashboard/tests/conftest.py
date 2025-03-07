import pytest
import ckan.tests.factories as factories
import ckan.model as model
from ckanext.dashboard.models import DatasetDashboard


@pytest.fixture
def clean_db(reset_db, migrate_db_for):
    """Clean and initialize the database."""
    reset_db()
    migrate_db_for("dashboard")


@pytest.fixture
def dashboard_test_data(clean_db):
    """Create test data specifically for dashboard tests."""
    sysadmin = factories.UserWithToken(sysadmin=True)
    sysadmin["headers"] = {"Authorization": sysadmin["token"]}

    user = factories.UserWithToken()
    user["headers"] = {"Authorization": user["token"]}

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
def dashboard_entry(dashboard_test_data):
    """
    Create a dashboard for the test dataset and return it.
    This dashboard can be used in update and delete tests.
    """
    dashboard = DatasetDashboard(
        package_id=dashboard_test_data.dataset["id"],
        dashboard_type="tableau",
        embeded_url="https://example.com/dashboard/embed?id=12345",
        report_url="https://example.com/dashboard/report?id=12345"
    )
    model.Session.add(dashboard)
    model.Session.commit()

    yield dashboard
