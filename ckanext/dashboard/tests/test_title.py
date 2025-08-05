from types import SimpleNamespace
import pytest
from ckan.lib.helpers import url_for
from ckan.tests import factories
from ckanext.dashboard.tests.factories import DashboardFactory


@pytest.fixture
def setup_data():
    """ TestFollowingTab setup data """
    obj = SimpleNamespace()
    """Create test data specifically for dashboard tests."""
    obj.user = factories.UserWithToken()
    obj.dataset = factories.Dataset()
    obj.dashboard = DashboardFactory(package_id=obj.dataset["id"], dashboard_type="tableau")

    return obj


@pytest.mark.usefixtures('with_plugins', 'clean_db')
class TestTitle:
    """ Test the dashboard title """

    @pytest.mark.ckan_config("ckanext.bcie.dashboard_title", "My dash title")
    def test_title_exists(self, app, setup_data):
        headers = {'Authorization': setup_data.user['token']}
        response = app.get(url_for("dataset.read", id=setup_data.dataset["name"]), headers=headers)
        assert "dashboard-title-class" in response
        assert 'My dash title' in response

    @pytest.mark.ckan_config("ckanext.bcie.dashboard_title", "")
    def test_empty_title(self, app, setup_data):
        headers = {'Authorization': setup_data.user['token']}
        response = app.get(url_for("dataset.read", id=setup_data.dataset["name"]), headers=headers)
        assert "dashboard-title-class" not in response
