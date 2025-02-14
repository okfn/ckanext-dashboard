import logging
import ckan.plugins as p
from flask import Blueprint, request, redirect, url_for, flash
from ckan.logic import NotFound
from ckan.plugins.toolkit import render

# Importa o define el decorador para restringir el acceso a sysadmins.
# Puedes definirlo en tu extensión o importarlo si ya lo tienes.
from ckanext.dashboard.decorators import require_sysadmin_user

log = logging.getLogger(__name__)

dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/', methods=['GET'])
@require_sysadmin_user
def index():
    """Listar las configuraciones de los dashboards"""
    log.debug("Listando configuraciones de dashboard")
    context = {'model': p.model, 'user': p.toolkit.c.user}
    try:
        dashboards = p.toolkit.get_action('dataset_dashboard_list')(context, {})
    except Exception as e:
        log.error("Error al listar dashboards: %s", e)
        dashboards = []
    return render('dashboard/index.html', extra_vars={'dashboards': dashboards})


@dashboard_bp.route('/edit/<package_id>', methods=['GET', 'POST'])
@require_sysadmin_user
def edit(package_id):
    """Editar la configuración de un dashboard para el dataset indicado"""
    log.debug("Editando dashboard para package_id: %s", package_id)
    context = {'model': p.model, 'user': p.toolkit.c.user}

    if request.method == 'POST':
        data = {
            'package_id': package_id,
            'embeded_url': request.form.get('embeded_url'),
            'report_url': request.form.get('report_url')
        }
        try:
            p.toolkit.get_action('dataset_dashboard_update')(context, data)
            flash('Dashboard updated successfully', 'success')
            log.info("Dashboard actualizado para package_id: %s", package_id)
        except Exception as e:
            flash('Error: {}'.format(e), 'error')
            log.error("Error actualizando dashboard para package_id %s: %s", package_id, e)
        return redirect(url_for('dashboard_bp.index'))
    else:
        try:
            dashboard = p.toolkit.get_action('dataset_dashboard_show')(context, {'package_id': package_id})
        except NotFound:
            dashboard = None
        return render('dashboard/edit.html', extra_vars={'dashboard': dashboard, 'package_id': package_id})


@dashboard_bp.route('/delete/<package_id>', methods=['POST'])
@require_sysadmin_user
def delete(package_id):
    """Eliminar la configuración de un dashboard para el dataset indicado"""
    log.debug("Eliminando dashboard para package_id: %s", package_id)
    context = {'model': p.model, 'user': p.toolkit.c.user}
    try:
        p.toolkit.get_action('dataset_dashboard_delete')(context, {'package_id': package_id})
        flash('Dashboard configuration deleted', 'success')
        log.info("Dashboard eliminado para package_id: %s", package_id)
    except Exception as e:
        flash('Error: {}'.format(e), 'error')
        log.error("Error eliminando dashboard para package_id %s: %s", package_id, e)
    return redirect(url_for('dashboard_bp.index'))
