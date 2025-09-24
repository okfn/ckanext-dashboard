import pytest
from ckan.plugins import toolkit
from ckan.tests import factories, helpers


@pytest.mark.usefixtures('with_plugins', 'clean_db')
class TestDashboardDatasetShowAuth:
    def test_public_dataset_is_viewable_by_anonymous(self):
        """Anyone can view the dashboard of a public dataset."""
        ds = factories.Dataset(private=False)
        context = {"user": ""}  # anonymous
        assert toolkit.check_access(
            "dataset_dashboard_show",
            context,
            {"pkg_id": ds["id"]},
        )

    def test_private_dataset_denied_to_anonymous(self):
        """Anonymous users cannot view the dashboard of a private dataset."""
        org = factories.Organization()
        ds = factories.Dataset(owner_org=org["id"], private=True)

        context = {"user": ""}  # anonymous
        with pytest.raises(toolkit.NotAuthorized):
            toolkit.check_access(
                "dataset_dashboard_show",
                context,
                {"pkg_id": ds["id"]},
            )

    def test_private_dataset_denied_to_non_member_user(self):
        """A non-member user cannot view the dashboard of a private dataset."""
        org = factories.Organization()
        ds = factories.Dataset(owner_org=org["id"], private=True)
        user = factories.User()

        context = {"user": user["name"]}
        with pytest.raises(toolkit.NotAuthorized):
            toolkit.check_access("dataset_dashboard_show", context, {"id": ds["id"]})

    def test_private_dataset_allowed_to_org_member(self):
        """A member user can view the dashboard of a private dataset."""
        org = factories.Organization()
        ds = factories.Dataset(owner_org=org["id"], private=True)
        user = factories.User()

        helpers.call_action(
            "organization_member_create",
            id=org["id"],
            username=user["name"],
            role="member",
        )

        context = {"user": user["name"]}
        assert toolkit.check_access("dataset_dashboard_show", context, {"id": ds["id"]}) is True

    def test_private_dataset_allowed_to_sysadmin(self):
        """A sysadmin can view the dashboard of a private dataset."""
        org = factories.Organization()
        ds = factories.Dataset(owner_org=org["id"], private=True)
        admin = factories.Sysadmin()

        context = {"user": admin["name"]}
        assert toolkit.check_access("dataset_dashboard_show", context, {"id": ds["id"]}) is True
