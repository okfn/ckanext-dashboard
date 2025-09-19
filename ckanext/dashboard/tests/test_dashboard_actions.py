import pytest
from ckan.plugins import toolkit as t
from ckan import model
from ckan.tests import helpers, factories
from ckanext.dashboard.models import DatasetDashboard


@pytest.fixture
def setup_data():
    """Creates sysadmin, regular user, organization and dataset."""
    data = {}
    data["sysadmin"] = factories.Sysadmin()
    data["user"] = factories.User()
    data["org"] = factories.Organization(user=data["sysadmin"])
    data["dataset"] = factories.Dataset(user=data["sysadmin"], owner_org=data["org"]["id"])
    return data


@pytest.mark.usefixtures('with_plugins', 'clean_db')
class TestDashboardActions:

    def test_show_not_found_raises_object_not_found(self, setup_data):
        """
        dataset_dashboard_show should raise ObjectNotFound if there is no dashboard
        for the specified pkg_id.
        """
        ctx = {"user": setup_data["sysadmin"]["name"]}
        with pytest.raises(t.ObjectNotFound, match=r"Dashboard not found\.?"):
            helpers.call_action(
                "dataset_dashboard_show",
                context=ctx,
                pkg_id=setup_data["dataset"]["id"],
            )

    def test_delete_not_found_raises_object_not_found(self, setup_data):
        """
        dataset_dashboard_delete should raise ObjectNotFound if the id does not exist.
        """
        ctx = {"user": setup_data["sysadmin"]["name"]}
        # non-existent id
        with pytest.raises(t.ObjectNotFound, match=r"Dashboard not found\.?"):
            helpers.call_action(
                "dataset_dashboard_delete",
                context=ctx,
                id=999999,
            )

    def test_show_success(self, setup_data):
        """Tests that dashboard is shown correctly."""
        # Create one directly in DB to test show
        session = model.Session
        dash = DatasetDashboard(
            package_id=setup_data["dataset"]["id"],
            dashboard_type="tableau",
            embeded_url="https://embed.example/d/1",
            report_url="https://report.example/r/1",
            report_title=None,  # to check default in show
        )
        session.add(dash)
        session.commit()

        ctx = {"user": setup_data["sysadmin"]["name"]}
        out = helpers.call_action(
            "dataset_dashboard_show",
            context=ctx,
            pkg_id=setup_data["dataset"]["id"],
        )
        assert out["id"] == dash.id
        assert out["package_id"] == setup_data["dataset"]["id"]
        assert out["dashboard_type"] == "tableau"
        assert out["embeded_url"] == "https://embed.example/d/1"
        assert out["report_url"] == "https://report.example/r/1"
        # default applied in the return
        assert out["report_title"] == "View full report"

    def test_show_not_authorized_when_dataset_is_private_and_user_not_in_org(self, setup_data):
        """Tests that dashboard cannot be viewed if dataset is private and user does not belong to the org."""
        # Private dataset -> users not in the org do not have package_show
        # Re-create a private dataset and a dashboard for that dataset
        private_ds = factories.Dataset(user=setup_data["sysadmin"], owner_org=setup_data["org"]["id"], private=True)
        session = model.Session
        dash = DatasetDashboard(
            package_id=private_ds["id"],
            dashboard_type="superset",
        )
        session.add(dash)
        session.commit()

        ctx = {"user": setup_data["user"]["name"], "ignore_auth": False}
        with pytest.raises(t.NotAuthorized):
            helpers.call_action(
                "dataset_dashboard_show",
                context=ctx,
                pkg_id=private_ds["id"],
            )

    # ----------------
    # CREATE
    # ----------------
    def test_create_requires_edit_permission(self, setup_data):
        """Tests that edit permission is required to create dashboard."""
        ctx = {"user": setup_data["user"]["name"], "ignore_auth": False}
        with pytest.raises(t.NotAuthorized):
            helpers.call_action(
                "dataset_dashboard_create",
                context=ctx,
                package_id=setup_data["dataset"]["id"],
                dashboard_type="tableau",
                embeded_url="https://embed.example/d/2",
                report_url="https://report.example/r/2",
                report_title="My report",
            )

    def test_create_dashboard_success_sysadmin(self, setup_data):
        """Tests successful dashboard creation by sysadmin."""
        # Sysadmin has edit permission on any dataset
        ctx = {"user": setup_data["sysadmin"]["name"]}
        out = helpers.call_action(
            "dataset_dashboard_create",
            context=ctx,
            package_id=setup_data["dataset"]["id"],
            dashboard_type="tableau",
            embeded_url="https://embed.example/d/2",
            report_url="https://report.example/r/2",
            report_title="My report",
        )
        assert out["package_id"] == setup_data["dataset"]["id"]
        assert out["dashboard_type"] == "tableau"
        assert out["embeded_url"] == "https://embed.example/d/2"
        assert out["report_url"] == "https://report.example/r/2"
        assert out["report_title"] == "My report"

        # Check persistence in DB
        session = model.Session
        db_obj = session.query(DatasetDashboard).filter_by(id=out["id"]).one()
        assert db_obj is not None

    # ----------------
    # UPDATE
    # ----------------
    def test_update_requires_edit_permission(self, setup_data):
        """Tests that edit permission is required to update dashboard."""
        # Seed
        session = model.Session
        dash = DatasetDashboard(
            package_id=setup_data["dataset"]["id"],
            dashboard_type="tableau",
        )
        session.add(dash)
        session.commit()

        ctx = {"user": setup_data["user"]["name"], "ignore_auth": False}
        with pytest.raises(t.NotAuthorized):
            helpers.call_action(
                "dataset_dashboard_update",
                context=ctx,
                package_id=setup_data["dataset"]["id"],
                report_title="New title",
            )

    def test_update_dashboard_success_sysadmin(self, setup_data):
        """Tests successful dashboard update by sysadmin."""
        # Seed
        session = model.Session
        dash = DatasetDashboard(
            package_id=setup_data["dataset"]["id"],
            dashboard_type="tableau",
            embeded_url="https://old/embed",
            report_url="https://old/report",
            report_title="Old title",
        )
        session.add(dash)
        session.commit()

        ctx = {"user": setup_data["sysadmin"]["name"]}
        out = helpers.call_action(
            "dataset_dashboard_update",
            context=ctx,
            package_id=setup_data["dataset"]["id"],
            dashboard_type="superset",
            embeded_url="https://new/embed",
            report_url="https://new/report",
            report_title="New title",
        )

        assert out["id"] == dash.id
        assert out["package_id"] == setup_data["dataset"]["id"]
        assert out["dashboard_type"] == "superset"
        assert out["embeded_url"] == "https://new/embed"
        assert out["report_url"] == "https://new/report"
        assert out["report_title"] == "New title"

        # Confirm in DB
        session.refresh(dash)
        assert dash.dashboard_type == "superset"
        assert dash.embeded_url == "https://new/embed"
        assert dash.report_url == "https://new/report"
        assert dash.report_title == "New title"

    def test_update_dashboard_not_found(self, setup_data):
        """Tests that update fails if dashboard does not exist."""
        ctx = {"user": setup_data["sysadmin"]["name"]}
        with pytest.raises(t.ObjectNotFound, match="Dashboard not found"):
            helpers.call_action(
                "dataset_dashboard_update",
                context=ctx,
                package_id=setup_data["dataset"]["id"],  # no dashboard created
                report_title="x",
            )

    # ----------------
    # DELETE
    # ----------------
    def test_delete_requires_edit_permission(self, setup_data):
        """Tests that edit permission is required to delete dashboard."""
        # Seed
        session = model.Session
        dash = DatasetDashboard(
            package_id=setup_data["dataset"]["id"],
            dashboard_type="tableau",
        )
        session.add(dash)
        session.commit()

        ctx = {"user": setup_data["user"]["name"], "ignore_auth": False}
        with pytest.raises(t.NotAuthorized):
            helpers.call_action(
                "dataset_dashboard_delete",
                context=ctx,
                id=dash.id,
            )

    def test_delete_success_sysadmin(self, setup_data):
        """Tests successful dashboard deletion by sysadmin."""
        # Seed
        session = model.Session
        dash = DatasetDashboard(
            package_id=setup_data["dataset"]["id"],
            dashboard_type="tableau",
        )
        session.add(dash)
        session.commit()

        ctx = {"user": setup_data["sysadmin"]["name"]}
        out = helpers.call_action(
            "dataset_dashboard_delete",
            context=ctx,
            id=dash.id,
        )
        assert out["success"] is True

        # Should no longer exist
        deleted = (
            model.Session.query(DatasetDashboard)
            .filter_by(id=dash.id)
            .first()
        )
        assert deleted is None
