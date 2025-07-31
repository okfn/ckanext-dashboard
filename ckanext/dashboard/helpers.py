from ckan import model
from ckan.plugins.toolkit import config

from ckanext.dashboard.models import DatasetDashboard


def get_dataset_dashboard(package_id):
    session = model.Session
    return session.query(DatasetDashboard).filter_by(package_id=package_id).first()


def get_dashboard_title_from_config():
    """Obtiene el título del dashboard desde la configuración del .ini"""
    return config.get('ckanext.dashboard.title', '')
