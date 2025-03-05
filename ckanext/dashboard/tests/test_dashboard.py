from types import SimpleNamespace
import pytest
from ckan.lib.helpers import url_for
from ckan.tests import factories


@pytest.fixture
def dashboard_test_data():
    """Setup basic data needed for dashboard tests including:
    - sysadmin user with token for admin operations
    - regular user with token for permission testing
    - dataset that will be used for dashboard attachment"""
    obj = SimpleNamespace()
    obj.sysadmin = factories.SysadminWithToken()
    obj.user = factories.UserWithToken()
    obj.dataset = factories.Dataset()
    return obj


@pytest.mark.usefixtures('with_plugins', 'clean_db')
class TestDashboard:
    """ Test dashboard functionality """

    def test_sysadmin_can_see_dashboard_icon(self, app, dashboard_test_data):
        """Test that sysadmins can see the dashboard icon on dataset pages,
        verifying the proper rendering of navigation elements for admins"""
        auth = {"Authorization": dashboard_test_data.sysadmin["token"]}
        url = url_for("dataset.read", id=dashboard_test_data.dataset["name"])
        response = app.get(url, extra_environ=auth)
        assert f'href="/dataset/dashboard/{dashboard_test_data.dataset["id"]}"' in response
        assert "Dashboard" in response

    def test_sysadmin_can_see_dashboard_form(self, app, dashboard_test_data):
        """Test that sysadmins can access the dashboard creation form,
        verifying form elements are properly rendered"""
        auth = {"Authorization": dashboard_test_data.sysadmin["token"]}
        url = url_for("dataset_dashboard.edit", package_id=dashboard_test_data.dataset["id"])
        response = app.get(url, extra_environ=auth)
        assert "Save" in response
        assert "Dashboard URL" in response

    def test_sysadmin_can_add_dashboard(self, app, dashboard_test_data):
        """Test that sysadmins can successfully add a dashboard to a dataset,
        and verify the dashboard appears correctly on the dataset page"""
        auth = {"Authorization": dashboard_test_data.sysadmin["token"]}
        url = url_for("dataset_dashboard.edit", package_id=dashboard_test_data.dataset["id"])
        dashboard_url = "https://example.com/dashboard/embed?id=12345"
        response = app.post(
            url,
            data={
                "embeded_url": dashboard_url,
                "title": "Test Dashboard"
            },
            extra_environ=auth
        )
        assert dashboard_url in response.body
        assert "Delete" in response.body
        
        # Verify dashboard appears on dataset page
        response = app.get(
            url_for("dataset.read", id=dashboard_test_data.dataset["name"]),
            extra_environ=auth,
        )
        assert "Dashboard" in response.body
        assert dashboard_url in response.body

    def test_normal_user_cannot_add_dashboard(self, app, dashboard_test_data):
        """Test that regular users cannot see or access dashboard functionality,
        verifying proper access control is in place"""
        auth = {"Authorization": dashboard_test_data.user["token"]}
        url = url_for("dataset.read", id=dashboard_test_data.dataset["name"])
        response = app.get(url, extra_environ=auth)
        assert f'href="/dataset/dashboard/{dashboard_test_data.dataset["id"]}"' not in response
        
        # Attempting to access dashboard edit page should fail
        url = url_for("dataset_dashboard.edit", package_id=dashboard_test_data.dataset["id"])
        response = app.get(url, extra_environ=auth, status=403)
        assert response.status_int == 403

    def test_dashboard_metadata_is_displayed(self, app, dashboard_test_data):
        """Test that dashboard metadata (title, description) is properly displayed
        in the dataset page when a dashboard is attached"""
        auth = {"Authorization": dashboard_test_data.sysadmin["token"]}
        url = url_for("dataset_dashboard.edit", package_id=dashboard_test_data.dataset["id"])
        response = app.post(
            url,
            data={
                "embeded_url": "https://example.com/dashboard/embed?id=12345",
                "title": "Test Dashboard",
                "description": "Dashboard description"
            },
            extra_environ=auth
        )
        response = app.get(
            url_for("dataset.read", id=dashboard_test_data.dataset["name"]),
            extra_environ=auth,
        )
        assert "Test Dashboard" in response.body
        assert "Dashboard description" in response.body

    def test_dashboard_can_be_updated(self, app, dashboard_test_data):
        """Test that an existing dashboard can be successfully updated,
        verifying that the new information is displayed correctly"""
        auth = {"Authorization": dashboard_test_data.sysadmin["token"]}
        url = url_for("dataset_dashboard.edit", package_id=dashboard_test_data.dataset["id"])
        
        # First create a dashboard
        response = app.post(
            url,
            data={
                "embeded_url": "https://example.com/dashboard/embed?id=12345",
                "title": "Original Title"
            },
            extra_environ=auth
        )
        
        # Then update it
        response = app.post(
            url,
            data={
                "embeded_url": "https://example.com/dashboard/embed?id=67890",
                "title": "Updated Title"
            },
            extra_environ=auth
        )
        
        # Check that the update was successful
        response = app.get(
            url_for("dataset.read", id=dashboard_test_data.dataset["name"]),
            extra_environ=auth,
        )
        assert "https://example.com/dashboard/embed?id=67890" in response.body
        assert "Updated Title" in response.body
        assert "https://example.com/dashboard/embed?id=12345" not in response.body

    def test_dashboard_can_be_deleted(self, app, dashboard_test_data):
        """Test that a dashboard can be successfully deleted,
        verifying that the dashboard no longer appears on the dataset page"""
        auth = {"Authorization": dashboard_test_data.sysadmin["token"]}
        url = url_for("dataset_dashboard.edit", package_id=dashboard_test_data.dataset["id"])
        
        # First create a dashboard
        response = app.post(
            url,
            data={
                "embeded_url": "https://example.com/dashboard/embed?id=12345",
                "title": "Test Dashboard"
            },
            extra_environ=auth
        )
        
        # Then delete it
        delete_url = url_for("dataset_dashboard.delete", package_id=dashboard_test_data.dataset["id"])
        response = app.post(delete_url, extra_environ=auth)
        
        # Check that the dashboard was deleted
        response = app.get(
            url_for("dataset.read", id=dashboard_test_data.dataset["name"]),
            extra_environ=auth,
        )
        assert "https://example.com/dashboard/embed?id=12345" not in response.body
        
        # Verify dashboard form is empty
        response = app.get(url, extra_environ=auth)
        assert 'value="https://example.com/dashboard/embed?id=12345"' not in response.body

    def test_dashboard_validation(self, app, dashboard_test_data):
        """Test validation of dashboard URLs,
        verifying that invalid URLs are properly rejected"""
        auth = {"Authorization": dashboard_test_data.sysadmin["token"]}
        url = url_for("dataset_dashboard.edit", package_id=dashboard_test_data.dataset["id"])
        
        # Test with invalid URL
        response = app.post(
            url,
            data={
                "embeded_url": "invalid-url",
                "title": "Test Dashboard"
            },
            extra_environ=auth
        )
        assert "Invalid URL format" in response.body

    def test_multiple_dashboards_for_dataset(self, app, dashboard_test_data):
        """Test support for multiple dashboards per dataset,
        verifying that all dashboards are properly displayed"""
        # This test assumes your extension supports multiple dashboards per dataset
        auth = {"Authorization": dashboard_test_data.sysadmin["token"]}
        url = url_for("dataset_dashboard.new", package_id=dashboard_test_data.dataset["id"])
        
        # Add first dashboard
        response = app.post(
            url,
            data={
                "embeded_url": "https://example.com/dashboard/embed?id=12345",
                "title": "First Dashboard"
            },
            extra_environ=auth
        )
        
        # Add second dashboard
        response = app.post(
            url,
            data={
                "embeded_url": "https://example.com/dashboard/embed?id=67890",
                "title": "Second Dashboard"
            },
            extra_environ=auth
        )
        
        # Check both dashboards appear
        response = app.get(
            url_for("dataset.read", id=dashboard_test_data.dataset["name"]),
            extra_environ=auth,
        )
        assert "First Dashboard" in response.body
        assert "Second Dashboard" in response.body
        assert "https://example.com/dashboard/embed?id=12345" in response.body
        assert "https://example.com/dashboard/embed?id=67890" in response.body
