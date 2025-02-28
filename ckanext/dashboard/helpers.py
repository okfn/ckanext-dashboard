from ckan import model

from ckanext.dashboard.models import DatasetDashboard


def get_dataset_dashboard(package_id):
    session = model.Session
    return session.query(DatasetDashboard).filter_by(package_id=package_id).first()
