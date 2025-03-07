import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from ckanext.dashboard.blueprints.dashboard import dashboard_bp
from ckanext.dashboard.actions.dashboard_dataset import (
    dataset_dashboard_create, dataset_dashboard_update, dataset_dashboard_delete,
    dataset_dashboard_show
)
from ckanext.dashboard.auth import dashboard_dataset as auth
from ckanext.dashboard.helpers import get_dataset_dashboard
from ckan.lib.plugins import DefaultTranslation


class DashboardPlugin(p.SingletonPlugin, DefaultTranslation):
    """Plugin for managing dashboards in CKAN"""
    p.implements(p.IConfigurer)
    p.implements(p.IBlueprint)
    p.implements(p.IActions)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IAuthFunctions)
    p.implements(p.ITranslation)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "dashboard")

    def get_blueprint(self):
        return dashboard_bp

    # IAuthFunctions

    def get_auth_functions(self):
        functions = {
            "dataset_dashboard_show": auth.dashboard_dataset_show,
            "dataset_dashboard_create": auth.dashboard_dataset_create,
            "dataset_dashboard_update": auth.dashboard_dataset_update,
            "dataset_dashboard_delete": auth.dashboard_dataset_delete,
        }
        return functions

    def get_actions(self):
        return {
            'dataset_dashboard_show': dataset_dashboard_show,
            'dataset_dashboard_create': dataset_dashboard_create,
            'dataset_dashboard_update': dataset_dashboard_update,
            'dataset_dashboard_delete': dataset_dashboard_delete
        }

    def get_helpers(self):
        return {'get_dataset_dashboard': get_dataset_dashboard}

    def i18n_locales(self):
        """Lanaguages this plugin has translations for."""
        # Return a list of languages that this plugin has translations for.
        return ["es", "en"]

    def i18n_domain(self):
        """The domain for this plugin's translations."""
        # Return the translation domain for this plugin.
        return "ckanext-dashboard"
