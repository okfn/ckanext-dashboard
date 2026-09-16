from functools import wraps
from ckan.plugins import toolkit


def require_sysadmin_user(func):
    '''
    Decorator for flask view functions. Returns 403 response if no user is logged in or if the login user is not sysadmin.
    '''

    @wraps(func)
    def view_wrapper(*args, **kwargs):
        user = toolkit.current_user
        if not getattr(user, "name", None):
            return toolkit.abort(403, "Forbidden")
        if not user.sysadmin:
            return toolkit.abort(403, "Sysadmin user required")
        return func(*args, **kwargs)

    return view_wrapper
