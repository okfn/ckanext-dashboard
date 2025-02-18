"""
Dashboard auth functions
"""


def dashboard_dataset_list(context, data_dict):
    """ Sysadmin only """
    return {'success': False}


def dashboard_dataset_create(context, data_dict):
    """Only sysadmins are allowed"""
    user_obj = context.get("auth_user_obj")
    return {"success": user_obj.sysadmin}


def dashboard_dataset_update(context, data_dict):
    """Only sysadmins are allowed"""
    user_obj = context.get("auth_user_obj")
    return {"success": user_obj.sysadmin}


def dashboard_dataset_delete(context, data_dict):
    """Only sysadmins are allowed"""
    user_obj = context.get("auth_user_obj")
    return {"success": user_obj.sysadmin}


def dashboard_dataset_show(context, data_dict):
    return {"success": True}
