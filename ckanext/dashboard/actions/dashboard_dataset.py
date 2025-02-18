import logging
from ckan.plugins import toolkit
from ckan import model
from ckanext.dashboard.models import DatasetDashboard

log = logging.getLogger(__name__)


@toolkit.side_effect_free
def dataset_dashboard_list(context, data_dict):
    """
    Devuelve la lista de configuraciones de dashboard almacenadas en la base de datos.

    Esta acción es side_effect_free (no tiene efectos colaterales) y verifica
    que el usuario tenga permisos para listar las configuraciones.
    """
    toolkit.check_access('dataset_dashboard_list', context, data_dict)

    session = model.Session
    dashboards = session.query(DatasetDashboard).all()
    result = []
    for dash in dashboards:
        result.append({
            'dashboard_id': dash.id,
            'package_id': dash.package_id,
            'embeded_url': dash.embeded_url,
            'report_url': dash.report_url,
        })
    log.debug("Se han recuperado %d configuraciones de dashboard", len(result))
    return result
