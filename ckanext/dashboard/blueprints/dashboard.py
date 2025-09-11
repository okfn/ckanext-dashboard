import logging
from ckan import model
import ckan.plugins as p
from flask import Blueprint, request, redirect, url_for
from ckan.plugins import toolkit
from ckan.lib.helpers import helper_functions as h

# Import or define the decorator to restrict access to sysadmins.
# You can define it in your extension or import it if you already have it.
from ckanext.dashboard.decorators import require_sysadmin_user

log = logging.getLogger(__name__)

dashboard_bp = Blueprint('embeded_dashboard', __name__)


def _must_edit_pkg_or_403(package_id):
    context = {'model': model, 'user': toolkit.c.user}
    try:
        toolkit.check_access('package_update', context, {'id': package_id})
    except toolkit.NotAuthorized:
        # Devolver una respuesta HTTP 403 Forbidden
        toolkit.abort(403, 'Not authorized to edit this dataset')


@dashboard_bp.route('/dataset/dashboard/<package_id>', methods=['GET', 'POST'], endpoint='create')
def dashboard_create(package_id):
    """Create a new dashboard (view and logic for creation)"""
    _must_edit_pkg_or_403(package_id)
    log.debug("Creating a new dashboard")
    try:
        pkg_dict = toolkit.get_action('package_show')({}, {'id': package_id})
    except toolkit.ObjectNotFound:
        h.flash_error('El dataset no existe.', 'error')
        return redirect(url_for('package.read', id=package_id))

    # Se capturan ambos tipos de excepciones: ObjectNotFound y ValueError
    try:
        dashboard_dict = toolkit.get_action('dataset_dashboard_show')({}, {'pkg_id': package_id})
    except (toolkit.ObjectNotFound, ValueError):
        dashboard_dict = {}

    if request.method == 'POST':
        data = {
            'package_id': pkg_dict['id'],
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'dashboard_type': request.form.get('dashboard_type', 'tableau'),
            'embeded_url': request.form.get('embeded_url'),
            'report_url': request.form.get('report_url'),
            'report_title': request.form.get('report_title', 'View full report'),
        }
        context = {'model': model, 'user': p.toolkit.c.user}
        toolkit.check_access('package_update', context, {'id': package_id})
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
    return toolkit.render('dashboard/form.html', {"pkg_dict": pkg_dict, "dashboard": dashboard_dict})


@dashboard_bp.route('/delete/<package_id>/<dashboard_id>', methods=['POST'], endpoint='dashboard_delete')
@require_sysadmin_user
def dashboard_delete(package_id, dashboard_id):
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
    return redirect(url_for('dataset.read', id=package_id))
