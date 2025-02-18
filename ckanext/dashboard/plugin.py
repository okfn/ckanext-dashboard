import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from ckan import model
from .blueprints.dashboard import dashboard_bp
from .models import DatasetDashboard
from .logic import dashboard
from ckanext.dashboard.auth import dashboard_dataset as auth


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

    def get_blueprint(self):
        return dashboard_bp

    # IAuthFunctions

    def get_auth_functions(self):
        functions = {
            "dashboard_dataset_list": auth.dashboard_dataset_list,
            "dashboard_dataset_create": auth.dashboard_dataset_create,
            "dashboard_dataset_show": auth.dashboard_dataset_show,
            "dashboard_dataset_update": auth.dashboard_dataset_update,
            "dashboard_dataset_delete": auth.dashboard_dataset_delete,
        }
        return functions

    def get_actions(self):
        return {
            'dataset_dashboard_list': dashboard.dataset_dashboard_list,
            'dataset_dashboard_create': dashboard.dataset_dashboard_create,
            'dataset_dashboard_show': dashboard.dataset_dashboard_show,
            'dataset_dashboard_update': dashboard.dataset_dashboard_update,
            'dataset_dashboard_delete': dashboard.dataset_dashboard_delete
        }

    def get_helpers(self):
        return {'get_dataset_dashboard': self.get_dataset_dashboard}

    def get_dataset_dashboard(self, package_id):
        session = model.Session
        return session.query(DatasetDashboard).filter_by(package_id=package_id).first()
