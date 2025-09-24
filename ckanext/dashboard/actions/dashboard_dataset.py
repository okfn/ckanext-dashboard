import logging
from ckan.plugins import toolkit
from ckan import model
from ckanext.dashboard.models import DatasetDashboard

log = logging.getLogger(__name__)


@toolkit.side_effect_free
def dataset_dashboard_show(context, data_dict):
    """
    Returns details of a specific dashboard for the given dataset (by pkg_id).

    :param context: Dictionary with action context information.
    :param data_dict: Dictionary with input data, must include 'pkg_id'.
    :return: Dictionary with dashboard details.
    """
    log.info("Executing dataset_dashboard_show")
    toolkit.check_access('dataset_dashboard_show', context, data_dict)

    pkg_id = toolkit.get_or_bust(data_dict, 'pkg_id')

    session = model.Session
    dashboard = session.query(DatasetDashboard).filter_by(package_id=pkg_id).first()

    if not dashboard:
        raise toolkit.ObjectNotFound("Dashboard not found.")

    return {
        'id': dashboard.id,
        'package_id': dashboard.package_id,
        'embeded_url': dashboard.embeded_url,
        'report_url': dashboard.report_url,
        'dashboard_type': dashboard.dashboard_type,
        'report_title': dashboard.report_title or 'View full report',
    }


def dataset_dashboard_create(context, data_dict):
    """
    Creates a new dashboard for a dataset.

    Expected keys in `data_dict` include 'package_id' and 'dashboard_type',
    ut you can add other fields as needed.

    :param context: Dictionary with action context information.
    :param data_dict: Dictionary with input data for creating the dashboard.
    :return: Dictionary with the details of the newly created dashboard.
    """
    log.info("Executing dataset_dashboard_create")
    toolkit.check_access('dataset_dashboard_create', context, data_dict)

    # Validate required fields
    package_id, dashboard_type = toolkit.get_or_bust(
        data_dict, ['package_id', 'dashboard_type']
    )

    new_dashboard = DatasetDashboard(
        package_id=package_id,
        dashboard_type=dashboard_type,
        embeded_url=data_dict.get('embeded_url', ''),
        report_url=data_dict.get('report_url', ''),
        report_title=data_dict.get('report_title', 'View full report'),
    )

    session = model.Session
    session.add(new_dashboard)
    session.commit()

    return {
        'id': new_dashboard.id,
        'package_id': new_dashboard.package_id,
        'dashboard_type': dashboard_type,
        'embeded_url': new_dashboard.embeded_url,
        'report_url': new_dashboard.report_url,
        'report_title': new_dashboard.report_title
    }


def dataset_dashboard_update(context, data_dict):
    """
    Updates a specific dashboard.

    :param context: Dictionary with action context information.
    :param data_dict: Dictionary with input data, must include the package ID.
    :return: Dictionary with the updated dashboard details.
    """
    log.info("Executing dataset_dashboard_update")
    toolkit.check_access('dataset_dashboard_update', context, data_dict)

    package_id = toolkit.get_or_bust(data_dict, 'package_id')

    session = model.Session
    dashboard = session.query(DatasetDashboard).filter_by(package_id=package_id).first()

    if not dashboard:
        raise toolkit.ObjectNotFound("Dashboard not found.")

    if 'dashboard_type' in data_dict:
        dashboard.dashboard_type = data_dict['dashboard_type']
    if 'embeded_url' in data_dict:
        dashboard.embeded_url = data_dict['embeded_url']
    if 'report_url' in data_dict:
        dashboard.report_url = data_dict['report_url']
    if 'report_title' in data_dict:
        dashboard.report_title = data_dict['report_title'] or 'View full report'

    session.add(dashboard)
    session.commit()

    return {
        'id': dashboard.id,
        'package_id': dashboard.package_id,
        'dashboard_type': dashboard.dashboard_type,
        'embeded_url': dashboard.embeded_url,
        'report_url': dashboard.report_url,
        'report_title': dashboard.report_title or 'View full report',
    }


def dataset_dashboard_delete(context, data_dict):
    """
    Deletes a specific dashboard.

    :param context: Dictionary with action context information.
    :param data_dict: Dictionary with input data, must include the dashboard ID.
    :return: Dictionary confirming the deletion.
    """
    log.info("Executing dataset_dashboard_delete")

    dashboard_id = data_dict['id']

    session = model.Session
    dashboard = session.query(DatasetDashboard).filter_by(id=dashboard_id).first()

    if not dashboard:
        raise toolkit.ObjectNotFound("Dashboard not found.")

    # Authorize using the package_id from the loaded dashboard
    data_dict['package_id'] = dashboard.package_id
    t.check_access('dataset_dashboard_delete', context, data_dict)

    session.delete(dashboard)
    session.commit()

    return {'success': True, 'message': 'Dashboard successfully deleted.'}
