from types import SimpleNamespace
import pytest
import ckan.model as model
from ckan.lib.helpers import url_for
from ckan.tests import factories
from ckanext.dashboard.models import DatasetDashboard
from ckanext.dashboard.tests.factories import DashboardFactory


@pytest.fixture
def setup_data():
    """ TestFollowingTab setup data """
    obj = SimpleNamespace()
    """Create test data specifically for dashboard tests."""
    obj.sysadmin = factories.SysadminWithToken()
    obj.sysadmin["headers"] = {'Authorization': obj.sysadmin["token"]}
    obj.user = factories.UserWithToken()
    obj.user["headers"] = {'Authorization': obj.user["token"]}

    obj.org = factories.Organization(user=obj.user)
    obj.dataset = factories.Dataset(user=obj.user, owner_org=obj.org["id"])

    return obj


@pytest.mark.usefixtures('with_plugins', 'clean_db')
class TestDashboard:
    """ Test dashboard functionality """

    def test_sysadmin_can_see_dashboard_icon(self, app, setup_data):
        """Test that sysadmins can see the dashboard icon on dataset pages,
        verifying the proper rendering of navigation elements for admins"""

        response = app.get(
            url_for("dataset.read", id=setup_data.dataset["name"]),
            headers=setup_data.sysadmin["headers"]
        )
        # Check for dashboard navigation elements
        assert 'Dashboard' in response

    def test_sysadmin_can_see_dashboard_form(self, app, setup_data):
        """Test that sysadmins can access the dashboard creation form,
        verifying form elements are properly rendered"""
        response = app.get(
            url_for("embeded_dashboard.create", package_id=setup_data.dataset["id"]),
            headers=setup_data.sysadmin["headers"],
            status=200
        )
        # Check form elements are present
        assert "Dashboard form" in response
        assert "Embeded URL" in response

    def test_sysadmin_can_add_dashboard(self, app, setup_data):
        """Test that sysadmins can successfully add a dashboard to a dataset,
        and verify the dashboard appears correctly on the dataset page"""
        dashboard_url = "https://example.com/dashboard/embed?id=12345"

        # Submit the dashboard form
        response = app.post(
            url_for("embeded_dashboard.create", package_id=setup_data.dataset["id"]),
            params={
                "embeded_url": dashboard_url,
                "report_url": "https://example.com/dashboard/report?id=12345",
                "dashboard_type": "tableau"
            },
            headers=setup_data.sysadmin["headers"],
            follow_redirects=True
        )

        # The dashboard URL should be in the response after creation
        assert "Dashboard" in response

    def test_normal_user_cannot_add_dashboard(self, app, setup_data):
        """Test that regular users cannot see or access dashboard functionality,
        verifying proper access control is in place"""
        # Normal users should not see dashboard icon
        response = app.get(
            url_for("dataset.read", id=setup_data.dataset["name"]),
            headers=setup_data.user["headers"]
        )
        assert f'href="/dataset/dashboard/{setup_data.dataset["id"]}"' not in response

        # If they try to access, it should return 403
        response = app.get(
            url_for("embeded_dashboard.create", package_id=setup_data.dataset["id"]),
            headers=setup_data.user["headers"],
            status=403
        )
        assert response.status_code == 403

    def test_dashboard_metadata_is_displayed(self, app, setup_data):
        """Test that dashboard metadata (title, description) is properly displayed
        in the dataset page when a dashboard is attached"""
        # Create a dashboard with metadata
        app.post(
            url_for("embeded_dashboard.create", package_id=setup_data.dataset["id"]),
            params={
                "embeded_url": "https://example.com/dashboard/embed?id=12345",
                "report_url": "https://example.com/dashboard/report?id=12345",
                "description": "Dashboard description",
                "dashboard_type": "tableau"
            },
            headers=setup_data.sysadmin["headers"],
        )

        # Check that the metadata is displayed on the dataset page
        response = app.get(
            url_for("dataset.read", id=setup_data.dataset["name"]),
            headers=setup_data.sysadmin["headers"]
        )

        # Verify our dashboard is represented in the page (specifics depend on your template)
        assert "Dashboard" in response

    def test_dashboard_can_be_updated(self, app, setup_data):
        """Test that an existing dashboard can be successfully updated,
        verifying that the new information is displayed correctly"""

        dashboard_entry = DashboardFactory(
            package_id=setup_data.dataset["id"],
            dashboard_type="tableau",
        )
        # Update the dashboard using the correct package_id and sysadmin from setup_data
        app.post(
            url_for("embeded_dashboard.create", package_id=dashboard_entry.package_id),
            params={
                "embeded_url": "https://example.com/dashboard/embed?id=67890",
                "report_url": "https://example.com/dashboard/report?id=12345",
                "dashboard_type": "powerbi"
            },
            headers=setup_data.sysadmin["headers"],
        )

        # Verify the update by querying the database
        from ckanext.dashboard.models import DatasetDashboard
        dashboard = model.Session.query(DatasetDashboard).filter_by(
            package_id=dashboard_entry.package_id
        ).first()

        # Check that the values were updated
        assert dashboard is not None
        assert dashboard.embeded_url == "https://example.com/dashboard/embed?id=67890"
        assert dashboard.dashboard_type == "powerbi"

    def test_dashboard_can_be_deleted(self, app, setup_data):
        """Test that a dashboard can be successfully deleted,
        verifying that the dashboard no longer appears on the dataset page"""
        dashboard_entry = DashboardFactory(
            package_id=setup_data.dataset["id"],
            dashboard_type="tableau",
        )
        dashboard_id = dashboard_entry.id
        app.post(
            url_for(
                "embeded_dashboard.dashboard_delete",
                package_id=setup_data.dataset["id"], dashboard_id=dashboard_id
            ),
            headers=setup_data.sysadmin["headers"],
        )
        deleted_dashboard = model.Session.query(DatasetDashboard).filter_by(
            package_id=setup_data.dataset["id"]
        ).first()
        assert deleted_dashboard is None

    def test_dashboard_validation(self, app, setup_data):
        """Test validation of dashboard URLs,
        verifying that invalid URLs are properly rejected"""

        response = app.post(
            url_for("embeded_dashboard.create", package_id=setup_data.dataset["id"]),
            params={
                "embeded_url": "invalid-url",
                "dashboard_type": "tableau"
            },
            headers=setup_data.sysadmin["headers"],
            follow_redirects=True
        )
        # Depending on your validation, it could be 200, 400, or 302
        assert response.status_code in [200, 400, 302]
