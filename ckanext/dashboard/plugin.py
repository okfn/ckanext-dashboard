import ckan.plugins as p
from ckan.plugins.toolkit import model
from .blueprints.dashboard import dashboard_bp
from .models import DatasetDashboard
from .logic import dashboard


class DashboardPlugin(p.SingletonPlugin):
    """Plugin para el manejo de dashboards en CKAN"""
    p.implements(p.IConfigurer)
    p.implements(p.IBlueprint)
    p.implements(p.IActions)
    p.implements(p.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        p.toolkit.add_template_directory(config_, "templates")
        p.toolkit.add_public_directory(config_, "public")
        p.toolkit.add_resource("assets", "dashboard")

    def get_blueprint(self):
        return dashboard_bp

    def get_actions(self):
        return {
            'dataset_dashboard_list': dashboard.dataset_dashboard_list,
            'dataset_dashboard_show': dashboard.dataset_dashboard_show,
            'dataset_dashboard_update': dashboard.dataset_dashboard_update,
            'dataset_dashboard_delete': dashboard.dataset_dashboard_delete
        }

    def get_helpers(self):
        return {'get_dataset_dashboard': self.get_dataset_dashboard}

    def get_dataset_dashboard(self, package_id):
        session = model.Session
        return session.query(DatasetDashboard).filter_by(package_id=package_id).first()
