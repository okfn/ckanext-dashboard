import logging
from ckan import model
from .models import DatasetDashboard
from ckan.plugins import SingletonPlugin, implements, IConfigurer

log = logging.getLogger(__name__)


class Dashboard(SingletonPlugin):
    """
    Clase Dashboard para la extensión ckanext-dashboard.
    Esta clase implementa la interfaz IConfigurer para actualizar la configuración de CKAN.
    Puedes extenderla implementando otras interfaces según tus necesidades.
    """

    # Implementa IConfigurer para modificar la configuración de CKAN
    implements(IConfigurer, inherit=True)

    def update_config(self, config):
        """
        Actualiza la configuración de CKAN, por ejemplo, añadiendo rutas de plantillas.
        """
        log.info("Dashboard: Actualizando configuración de CKAN")
        # Ejemplo: agregar un directorio de plantillas personalizado para el dashboard
        dashboard_template_path = '/app/ckanext/dashboard/templates'
        if 'extra_template_paths' in config:
            config['extra_template_paths'] += ';' + dashboard_template_path
        else:
            config['extra_template_paths'] = dashboard_template_path

    @staticmethod
    def dataset_dashboard_list(context, data_dict):
        """
        Acción personalizada que retorna una lista de dashboards asociados a un dataset.

        Se espera que en data_dict se incluya la clave 'id' que corresponde al identificador
        del dataset (package_id). La función consulta la base de datos y retorna una lista de
        diccionarios, donde cada diccionario representa un dashboard.

        :param context: Diccionario con información del contexto de la acción.
        :param data_dict: Diccionario con los datos de entrada de la acción, debe incluir 'id'.
        :return: Lista de diccionarios con la información de cada dashboard.
        """
        log = logging.getLogger(__name__)
        log.info("Ejecutando acción dataset_dashboard_list")

        # Validar que se haya proporcionado el identificador del dataset
        dataset_id = data_dict.get('id')
        if not dataset_id:
            raise ValueError("El parámetro 'id' es obligatorio en data_dict.")

        # Realiza la consulta a la base de datos para obtener todos los dashboards asociados
        session = model.Session
        dashboards = session.query(DatasetDashboard).filter_by(package_id=dataset_id).all()

        # Convierte cada objeto dashboard a un diccionario.
        # Se asume que el modelo DatasetDashboard tiene los atributos: id, package_id, title, description.
        dashboard_list = []
        for dashboard in dashboards:
            dashboard_dict = {
                'id': dashboard.id,
                'package_id': dashboard.package_id,
                'title': dashboard.title,
                'description': dashboard.description,
            }
            dashboard_list.append(dashboard_dict)

        log.info("Se encontraron %d dashboards para el dataset %s", len(dashboard_list), dataset_id)
        return dashboard_list

    @staticmethod
    def dataset_dashboard_show(context, data_dict):
        """
        Acción que retorna los detalles de un dashboard en particular.

        :param context: Diccionario con información del contexto de la acción.
        :param data_dict: Diccionario con los datos de entrada, que debe incluir
                          el identificador del dashboard o del dataset.
        :return: Diccionario con los detalles del dashboard (por defecto, vacío).
        """
        log = logging.getLogger(__name__)
        log.info("Ejecutando acción dataset_dashboard_show")

        dashboard_id = data_dict.get('id')
        if not dashboard_id:
            raise ValueError("El parámetro 'id' es obligatorio para mostrar el dashboard.")

        session = model.Session
        dashboard = session.query(DatasetDashboard).filter_by(id=dashboard_id).first()

        if not dashboard:
            raise ValueError("Dashboard no encontrado.")

        # Convierte el objeto dashboard a un diccionario con los campos necesarios.
        dashboard_dict = {
            'id': dashboard.id,
            'package_id': dashboard.package_id,
            'title': dashboard.title,
            'description': dashboard.description,
            # Agrega aquí otros campos que necesites exponer.
        }
        return dashboard_dict

    @staticmethod
    def dataset_dashboard_update(context, data_dict):
        """
        Acción que actualiza un dashboard en particular.

        :param context: Diccionario con información del contexto de la acción.
        :param data_dict: Diccionario con los datos de entrada, que debe incluir
                          el identificador del dashboard o del dataset y los datos a actualizar.
        :return: Diccionario con el resultado de la operación (por defecto, vacío).
        """
        log.info("Ejecutando acción dataset_dashboard_update")

        dashboard_id = data_dict.get('id')
        if not dashboard_id:
            raise ValueError("El parámetro 'id' es obligatorio para actualizar el dashboard.")

        session = model.Session
        dashboard = session.query(DatasetDashboard).filter_by(id=dashboard_id).first()

        if not dashboard:
            raise ValueError("Dashboard no encontrado.")

        # Actualiza los campos disponibles. Por ejemplo, actualizamos 'title' y 'description'
        if 'title' in data_dict:
            dashboard.title = data_dict['title']
        if 'description' in data_dict:
            dashboard.description = data_dict['description']
        # Agrega aquí la actualización de otros campos si es necesario.

        session.add(dashboard)
        session.commit()

        updated_dashboard = {
            'id': dashboard.id,
            'package_id': dashboard.package_id,
            'title': dashboard.title,
            'description': dashboard.description,
            # Incluye otros campos actualizados según corresponda.
        }
        return updated_dashboard

    @staticmethod
    def dataset_dashboard_delete(context, data_dict):
        """
        Acción que elimina un dashboard en particular.

        :param context: Diccionario con información del contexto de la acción.
        :param data_dict: Diccionario con los datos de entrada, que debe incluir
                          el identificador del dashboard o del dataset.
        :return: Diccionario con el resultado de la operación (por defecto, vacío).
        """
        log.info("Ejecutando acción dataset_dashboard_delete")
        dashboard_id = data_dict.get('id')
        if not dashboard_id:
            raise ValueError("El parámetro 'id' es obligatorio para eliminar el dashboard.")

        session = model.Session
        dashboard = session.query(DatasetDashboard).filter_by(id=dashboard_id).first()

        if not dashboard:
            raise ValueError("Dashboard no encontrado.")

        session.delete(dashboard)
        session.commit()

        return {'success': True, 'message': 'Dashboard eliminado correctamente.'}

    @staticmethod
    def dataset_dashboard_create(context, data_dict):
        """
        Acción que crea un dashboard para un dataset.

        Se espera que en data_dict se incluyan las claves necesarias para crear el dashboard,
        por ejemplo, 'package_id' y 'title'. La 'description' es opcional, pero puedes agregar
        otros campos según la definición de tu modelo.

        :param context: Diccionario con información del contexto de la acción.
        :param data_dict: Diccionario con los datos de entrada para crear el dashboard.
        :return: Diccionario con los detalles del dashboard recién creado.
        """

        log.info("Ejecutando acción dataset_dashboard_create")

        # Validar campos obligatorios
        required_fields = ['package_id', 'title']
        missing_fields = [field for field in required_fields if field not in data_dict]
        if missing_fields:
            raise ValueError("Faltan campos obligatorios: " + ", ".join(missing_fields))

        session = model.Session

        # Crear una nueva instancia del dashboard
        new_dashboard = DatasetDashboard(
            package_id=data_dict.get('package_id'),
            title=data_dict.get('title'),
            description=data_dict.get('description', '')  # 'description' es opcional
            # Agrega aquí otros campos según tu modelo
        )

        # Agrega la nueva instancia a la sesión y confirma la transacción
        session.add(new_dashboard)
        session.commit()

        # Retorna el dashboard creado convertido a diccionario
        created_dashboard = {
            'id': new_dashboard.id,
            'package_id': new_dashboard.package_id,
            'title': new_dashboard.title,
            'description': new_dashboard.description,
            # Incluye otros campos que necesites exponer
        }
        return created_dashboard


# Exporta la clase asignándola a la variable 'dashboard'
dashboard = Dashboard
