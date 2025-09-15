"""
Dashboard auth functions
"""

from ckan.plugins import toolkit


def _can_edit_pkg(context, data_dict):
    pkg_id = data_dict.get('id') or data_dict.get('package_id') or data_dict.get('pkg_id')
    if not pkg_id:
        return {"success": False}
    try:
        toolkit.check_access('package_update', context, {'id': pkg_id})
        return {"success": True}
    except toolkit.NotAuthorized:
        return {"success": False}


def dashboard_dataset_create(context, data_dict):
    return _can_edit_pkg(context, data_dict)


def dashboard_dataset_update(context, data_dict):
    return _can_edit_pkg(context, data_dict)


def dashboard_dataset_delete(context, data_dict):
    return _can_edit_pkg(context, data_dict)


def dashboard_dataset_show(context, data_dict):
    # Viewing the dashboard doesn't require editor permissions (adjust if needed)
    return {"success": True}
