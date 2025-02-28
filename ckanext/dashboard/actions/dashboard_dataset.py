import logging
import uuid
from ckan.plugins import toolkit
from ckan import model
from ckanext.dashboard.models import DatasetDashboard

log = logging.getLogger(__name__)


@toolkit.side_effect_free
def dataset_dashboard_list(context, data_dict):
    """
    Returns a list of dashboard configurations stored in the database.

    This action is side_effect_free (has no side effects) and ensures
    that the user has the necessary permissions to list dashboard configurations.
    """
    toolkit.check_access('dataset_dashboard_list', context, data_dict)

    session = model.Session
    dashboards = session.query(DatasetDashboard).all()
    result = []
    for dash in dashboards:
        result.append({
            'dashboard_id': dash.id,
            'title': dash.title,
            'description': dash.description,
            'package_id': dash.package_id,
            'embeded_url': dash.embeded_url,
            'report_url': dash.report_url,
        })
    log.debug("Retrieved %d dashboard configurations", len(result))
    return result


@toolkit.side_effect_free
def dataset_dashboard_show(context, data_dict):
    """
    Returns details of a specific dashboard.

    :param context: Dictionary with action context information.
    :param data_dict: Dictionary with input data, must include the dashboard ID.
    :return: Dictionary with dashboard details.
    """
    log.info("Executing dataset_dashboard_show")

    dashboard_id = toolkit.get_or_bust(data_dict, 'id')

    session = model.Session
    dashboard = session.query(DatasetDashboard).filter_by(id=dashboard_id).first()

    if not dashboard:
        raise ValueError("Dashboard not found.")

    return {
        'id': dashboard.id,
        'package_id': dashboard.package_id,
        'title': dashboard.title,
        'description': dashboard.description,
        'embeded_url': dashboard.embeded_url,
        'report_url': dashboard.report_url
    }


def dataset_dashboard_create(context, data_dict):
    """
    Creates a new dashboard for a dataset.

    Expected keys in `data_dict` include 'package_id' and 'title'.
    'description' is optional, but you can add other fields as needed.

    :param context: Dictionary with action context information.
    :param data_dict: Dictionary with input data for creating the dashboard.
    :return: Dictionary with the details of the newly created dashboard.
    """
    log.info("Executing dataset_dashboard_create")

    # Validate required fields
    package_id, title, dashboard_type = toolkit.get_or_bust(
            data_dict, ['package_id', 'title', 'dashboard_type']
            )

    new_dashboard = DatasetDashboard(
        package_id=package_id,
        title=data_dict.get('title'),
        description=data_dict.get('description', ''),
        dashboard_type=dashboard_type,
        embeded_url=data_dict.get('embeded_url', ''),
        report_url=data_dict.get('report_url', ''),
    )

    session = model.Session
    session.add(new_dashboard)
    session.commit()

    return {
        'id': new_dashboard.id,
        'package_id': new_dashboard.package_id,
        'title': new_dashboard.title,
        'description': new_dashboard.description,
        'dashboard_type': dashboard_type,
        'embeded_url': new_dashboard.embeded_url,
        'report_url': new_dashboard.report_url,
    }


def dataset_dashboard_update(context, data_dict):
    """
    Updates a specific dashboard.

    :param context: Dictionary with action context information.
    :param data_dict: Dictionary with input data, must include the dashboard ID.
    :return: Dictionary with the updated dashboard details.
    """
    log.info("Executing dataset_dashboard_update")

    dashboard_id = toolkit.get_or_bust(data_dict, 'dashboard_id')

    session = model.Session
    dashboard = session.query(DatasetDashboard).filter_by(id=dashboard_id).first()

    if not dashboard:
        raise ValueError("Dashboard not found.")

    if 'title' in data_dict:
        dashboard.title = data_dict['title']
    if 'description' in data_dict:
        dashboard.description = data_dict['description']
    # TODO: Handle dashboard_type
    if 'embeded_url' in data_dict:
        dashboard.embeded_url = data_dict['embeded_url']
    if 'report_url' in data_dict:
        dashboard.report_url = data_dict['report_url']

    session.add(dashboard)
    session.commit()

    return {
        'id': dashboard.id,
        'package_id': dashboard.package_id,
        'title': dashboard.title,
        'description': dashboard.description,
        'embeded_url': dashboard.embeded_url,
        'report_url': dashboard.report_url
    }


def dataset_dashboard_delete(context, data_dict):
    """
    Deletes a specific dashboard.

    :param context: Dictionary with action context information.
    :param data_dict: Dictionary with input data, must include the dashboard ID.
    :return: Dictionary confirming the deletion.
    """
    log.info("Executing dataset_dashboard_delete")

    dashboard_id = toolkit.get_or_bust(data_dict, 'id')

    session = model.Session
    dashboard = session.query(DatasetDashboard).filter_by(id=dashboard_id).first()

    if not dashboard:
        raise ValueError("Dashboard not found.")

    session.delete(dashboard)
    session.commit()

    return {'success': True, 'message': 'Dashboard successfully deleted.'}
