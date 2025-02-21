import logging
from ckan import model
import ckan.plugins as p
from flask import Blueprint, request, redirect, url_for, flash
from ckan.logic import NotFound
from ckan.plugins.toolkit import render

# Import or define the decorator to restrict access to sysadmins.
# You can define it in your extension or import it if you already have it.
from ckanext.dashboard.decorators import require_sysadmin_user

log = logging.getLogger(__name__)

dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard-external')


@dashboard_bp.route('/', methods=['GET'], endpoint='dashboard_list')
@require_sysadmin_user
def index():
    """List dashboard configurations"""
    log.debug("Listing dashboard configurations")
    context = {'model': model, 'user': p.toolkit.c.user}
    try:
        dashboards = p.toolkit.get_action('dataset_dashboard_list')(context, {})
    except Exception as e:
        log.error("Failed to load dashboards: %s", e)
        flash("An error occurred while retrieving the dashboards.", "error")
        dashboards = []
    return render('dashboard/index.html', extra_vars={'dashboards': dashboards})


@dashboard_bp.route('/new', methods=['GET', 'POST'], endpoint='dashboard_new')
@require_sysadmin_user
def dashboard_new():
    """Create a new dashboard (view and logic for creation)"""
    log.debug("Creating a new dashboard")
    if request.method == 'POST':
        data = {
            'package_id': request.form.get('package_id'),
            'title': request.form.get('title'),
            'embeded_url': request.form.get('embeded_url'),
            'report_url': request.form.get('report_url')
        }
        context = {'model': model, 'user': p.toolkit.c.user}
        try:
            p.toolkit.get_action('dataset_dashboard_create')(context, data)
            flash('Dashboard created successfully', 'success')
            log.info("Dashboard created")
        except Exception as e:
            flash(f'Error: {e}', 'error')
            log.error("Error creating dashboard: %s", e)
        return redirect(url_for('dashboard_bp.dashboard_list'))
    return render('dashboard/new.html')


@dashboard_bp.route('/edit/<dashboard_id>', methods=['GET', 'POST'], endpoint='dashboard_edit')
@require_sysadmin_user
def dashboard_edit(dashboard_id):
    """Edit the configuration of a dashboard using its unique ID"""
    log.debug("Editing dashboard for dashboard_id: %s", dashboard_id)
    context = {'model': model, 'user': p.toolkit.c.user}

    if request.method == 'POST':
        data = {
            'dashboard_id': dashboard_id,
            'embeded_url': request.form.get('embeded_url'),
            'report_url': request.form.get('report_url')
        }
        try:
            p.toolkit.get_action('dataset_dashboard_update')(context, data)
            flash('Dashboard updated successfully', 'success')
            log.info("Dashboard updated for dashboard_id: %s", dashboard_id)
        except Exception as e:
            flash(f'Error: {e}', 'error')
            log.error("Error updating dashboard for dashboard_id %s: %s", dashboard_id, e)
        return redirect(url_for('dashboard_bp.dashboard_list'))
    else:
        try:
            dashboard = p.toolkit.get_action('dataset_dashboard_show')(context, {'dashboard_id': dashboard_id})
        except NotFound:
            dashboard = None
        return render('dashboard/edit.html', extra_vars={'dashboard': dashboard, 'dashboard_id': dashboard_id})


@dashboard_bp.route('/delete/<dashboard_id>', methods=['POST'], endpoint='dashboard_delete')
@require_sysadmin_user
def dashboard_delete(dashboard_id):
    """Delete the configuration of a dashboard using its unique ID"""
    log.debug("Deleting dashboard for dashboard_id: %s", dashboard_id)
    context = {'model': model, 'user': p.toolkit.c.user}
    try:
        p.toolkit.get_action('dataset_dashboard_delete')(context, {'dashboard_id': dashboard_id})
        flash('Dashboard configuration deleted', 'success')
        log.info("Dashboard deleted for dashboard_id: %s", dashboard_id)
    except Exception as e:
        flash(f'Error: {e}', 'error')
        log.error("Error deleting dashboard for dashboard_id %s: %s", dashboard_id, e)
    return redirect(url_for('dashboard_bp.dashboard_list'))
