import logging
from ckan import model
import ckan.plugins as p
from flask import Blueprint, request, redirect, url_for
from ckan.logic import NotFound
from ckan.plugins import toolkit
from ckan.lib.helpers import helper_functions as h

# Import or define the decorator to restrict access to sysadmins.
# You can define it in your extension or import it if you already have it.
from ckanext.dashboard.decorators import require_sysadmin_user

log = logging.getLogger(__name__)

dashboard_bp = Blueprint('embeded_dashboard', __name__)


@dashboard_bp.route('/dataset/dashboard/<package_id>', methods=['GET', 'POST'], endpoint='create')
@require_sysadmin_user
def dashboard_create(package_id):
    """Create a new dashboard (view and logic for creation)"""
    log.debug("Creating a new dashboard")
    # TODO: try-catch
    pkg_dict = toolkit.get_action('package_show')({}, {'id': package_id})

    try:
        dashboard_dict = toolkit.get_action('dataset_dashboard_show')({}, {'pkg_id': package_id})
    except toolkit.ObjectNotFound:
        dashboard_dict = {}

    if request.method == 'POST':
        data = {
            'package_id': pkg_dict['id'],
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            # TODO: Add field in form
            'dashboard_type': 'tableau',
            'embeded_url': request.form.get('embeded_url'),
            'report_url': request.form.get('report_url')
        }
        context = {'model': model, 'user': p.toolkit.c.user}
        try:
            if not dashboard_dict:
                p.toolkit.get_action('dataset_dashboard_create')(context, data)
                h.flash_success('Dashboard created successfully', 'success')
                log.info("Dashboard created")
            else:
                toolkit.get_action('dataset_dashboard_update')(context, data)
                h.flash_success('Dashboard updated successfully', 'success')
                log.info("Dashboard updated")
        except Exception as e:
            h.flash_error(f'Error: {e}', 'error')
            log.error("Error creating dashboard: %s", e)
        return redirect(url_for('dataset.read', id=pkg_dict['id']))
    return toolkit.render('dashboard/new.html', {"pkg_dict": pkg_dict, "dashboard": dashboard_dict})


@dashboard_bp.route('/delete/<dashboard_id>', methods=['POST'], endpoint='dashboard_delete')
@require_sysadmin_user
def dashboard_delete(dashboard_id):
    """Delete the configuration of a dashboard using its unique ID"""
    log.debug("Deleting dashboard for dashboard_id: %s", dashboard_id)
    context = {'model': model, 'user': p.toolkit.c.user}
    try:
        p.toolkit.get_action('dataset_dashboard_delete')(context, {'id': dashboard_id})
        h.flash_success('Dashboard configuration deleted', 'success')
        log.info("Dashboard deleted for dashboard_id: %s", dashboard_id)
    except Exception as e:
        h.flash_error(f'Error: {e}', 'error')
        log.error("Error deleting dashboard for dashboard_id %s: %s", dashboard_id, e)
    return redirect(url_for('embeded_dashboard.dashboard_list'))


@dashboard_bp.route('/show/<dashboard_id>', methods=['GET'], endpoint='dashboard_show')
@require_sysadmin_user
def dashboard_show(dashboard_id):
    """Show the configuration of a dashboard using its unique ID"""
    log.debug("Showing dashboard for dashboard_id: %s", dashboard_id)
    context = {'model': model, 'user': p.toolkit.c.user}
    try:
        dashboard = p.toolkit.get_action('dataset_dashboard_show')(context, {'id': dashboard_id})
    except NotFound:
        dashboard = None
    return render('dashboard/show.html', extra_vars={'dashboard': dashboard, 'dashboard_id': dashboard_id})
