"""
Dashboard auth functions
"""

from ckan.plugins import toolkit


def _pkg_id_from(data_dict):
    return data_dict.get('id') or data_dict.get('package_id') or data_dict.get('pkg_id')


def _can_edit_pkg(context, data_dict):
    pkg_id = _pkg_id_from(data_dict)
    if not pkg_id:
        return {"success": False}
    try:
        toolkit.check_access('package_update', context, {'id': pkg_id})
        return {"success": True}
    except toolkit.NotAuthorized:
        return {"success": False}


def _can_view_pkg(context, data_dict):
    """Permite si el usuario puede hacer package_show sobre el dataset."""
    pkg_id = _pkg_id_from(data_dict)
    if not pkg_id:
        return {"success": False}
    try:
        toolkit.check_access('package_show', context, {'id': pkg_id})
        return {"success": True}
    except toolkit.NotAuthorized:
        return {"success": False}


def dashboard_dataset_create(context, data_dict):
    """Creating the dashboard requires permission to edit the dataset."""
    return _can_edit_pkg(context, data_dict)


def dashboard_dataset_update(context, data_dict):
    """Updating the dashboard requires permission to edit the dataset."""
    return _can_edit_pkg(context, data_dict)


def dashboard_dataset_delete(context, data_dict):
    """Deleting the dashboard requires permission to edit the dataset."""
    return _can_edit_pkg(context, data_dict)


@toolkit.auth_allow_anonymous_access
def dashboard_dataset_show(context, data_dict):
    """Viewing the dashboard requires permission to view the dataset."""
    return _can_view_pkg(context, data_dict)
