from ckan import model
from ckan.plugins import toolkit as t


from ckanext.dashboard.models import DatasetDashboard


def get_dataset_dashboard(package_id):
    session = model.Session
    return session.query(DatasetDashboard).filter_by(package_id=package_id).first()


def get_dashboard_title_from_config():
    """Obtiene el título del dashboard desde la configuración del .ini"""
    try:
        result = t.get_action('config_option_show')(
            {'ignore_auth': True},
            {'key': 'ckanext.bcie.dashboard_title'}
        )
        if result and result.get('value'):
            return result['value']
    except Exception:
        pass
    return t.config.get('ckanext.bcie.dashboard_title', '')
