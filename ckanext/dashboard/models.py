from sqlalchemy import Column, Integer, String
from ckan.plugins import toolkit
from ckan.model.base import ActiveRecordMixin

from ckan.model.types import UuidType


class DatasetDashboard(toolkit.BaseModel, ActiveRecordMixin):
    """Modelo de datos para almacenar la configuración de un dashboard por dataset"""
    __tablename__ = "ndx_dataset_dashboard"

    id = Column(Integer, primary_key=True)
    package_id = Column(UuidType, nullable=False, unique=True)
    embeded_url = Column(String(200))
    report_url = Column(String(200))
