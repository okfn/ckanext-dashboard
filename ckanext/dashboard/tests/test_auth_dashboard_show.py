import pytest
from ckan.plugins import toolkit
from ckan.tests import factories, helpers



@pytest.mark.usefixtures('with_plugins', 'clean_db')
class TestDashboardDatasetShowAuth:
    def test_public_dataset_is_viewable_by_anonymous(self):
        org = factories.Organization()
        ds = factories.Dataset(owner_org=org["id"], private=False)

        # anonymous
        context = {"user": ""}
        assert toolkit.check_access("dataset_dashboard_show", context, {"id": ds["id"]}) is True

    def test_private_dataset_denied_to_anonymous(self):
        org = factories.Organization()
        ds = factories.Dataset(owner_org=org["id"], private=True)

        context = {"user": ""}
        assert toolkit.check_access("dataset_dashboard_show", context, {"id": ds["id"]}) is False

    def test_private_dataset_denied_to_non_member_user(self):
        org = factories.Organization()
        ds = factories.Dataset(owner_org=org["id"], private=True)
        user = factories.User()

        context = {"user": user["name"]}
        assert toolkit.check_access("dataset_dashboard_show", context, {"id": ds["id"]}) is False

    def test_private_dataset_allowed_to_org_member(self):
        org = factories.Organization()
        ds = factories.Dataset(owner_org=org["id"], private=True)
        user = factories.User()

        # dar rol lector (member) en la org
        helpers.call_action(
            "organization_member_create",
            id=org["id"],
            username=user["name"],
            role="member",
        )

        context = {"user": user["name"]}
        assert toolkit.check_access("dataset_dashboard_show", context, {"id": ds["id"]}) is True

    def test_private_dataset_allowed_to_sysadmin(self):
        org = factories.Organization()
        ds = factories.Dataset(owner_org=org["id"], private=True)
        admin = factories.Sysadmin()

        context = {"user": admin["name"]}
        assert toolkit.check_access("dataset_dashboard_show", context, {"id": ds["id"]}) is True
