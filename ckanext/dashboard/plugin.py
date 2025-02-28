import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from ckanext.dashboard.blueprints.dashboard import dashboard_bp
from ckanext.dashboard.actions.dashboard_dataset import (dataset_dashboard_list,
                                                         dataset_dashboard_create,
                                                         dataset_dashboard_show,
                                                         dataset_dashboard_update,
                                                         dataset_dashboard_delete)
from ckanext.dashboard.auth import dashboard_dataset as auth
from ckanext.dashboard.helpers import get_dataset_dashboard


class DashboardPlugin(p.SingletonPlugin):
    """Plugin for managing dashboards in CKAN"""
    p.implements(p.IConfigurer)
    p.implements(p.IBlueprint)
    p.implements(p.IActions)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IAuthFunctions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "dashboard")
        dashboard_template_path = '/app/ckanext/dashboard/templates'
        if 'extra_template_paths' in config_:
            config_['extra_template_paths'] += ';' + dashboard_template_path
        else:
            config_['extra_template_paths'] = dashboard_template_path

    def get_blueprint(self):
        return dashboard_bp

    # IAuthFunctions

    def get_auth_functions(self):
        functions = {
            "dataset_dashboard_list": auth.dashboard_dataset_list,
            "dataset_dashboard_create": auth.dashboard_dataset_create,
            "dataset_dashboard_show": auth.dashboard_dataset_show,
            "dataset_dashboard_update": auth.dashboard_dataset_update,
            "dataset_dashboard_delete": auth.dashboard_dataset_delete,
        }
        return functions

    def get_actions(self):
        return {
            'dataset_dashboard_list': dataset_dashboard_list,
            'dataset_dashboard_create': dataset_dashboard_create,
            'dataset_dashboard_show': dataset_dashboard_show,
            'dataset_dashboard_update': dataset_dashboard_update,
            'dataset_dashboard_delete': dataset_dashboard_delete
        }

    def get_helpers(self):
        return {'get_dataset_dashboard': get_dataset_dashboard}
