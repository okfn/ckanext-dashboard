import logging
from ckan import model
from ckan.plugins import toolkit as t

from ckanext.dashboard.models import DatasetDashboard

log = logging.getLogger(__name__)


def get_dataset_dashboard(package_id):
    session = model.Session
    return session.query(DatasetDashboard).filter_by(package_id=package_id).first()


def get_dashboard_title_from_config():
    """Gets the dashboard title from the .ini configuration"""
    try:
        return t.config.get('ckanext.bcie.dashboard_title', '')
    except Exception as e:
        log.error(f"Error retrieving dashboard title from config: {e}")
        return ''
