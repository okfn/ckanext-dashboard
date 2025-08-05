import pytest
from ckan import plugins


@pytest.mark.ckan_config("ckan.plugins", "dashboard")
@pytest.mark.usefixtures("with_plugins")
def test_plugin():
    assert plugins.plugin_loaded("dashboard")
