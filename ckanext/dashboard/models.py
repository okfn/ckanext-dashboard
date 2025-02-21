from sqlalchemy import Column, Integer, String
from ckan.plugins import toolkit
from ckan.model.base import ActiveRecordMixin

from ckan.model.types import UuidType


class DatasetDashboard(toolkit.BaseModel, ActiveRecordMixin):
    """Data model for storing the configuration of a dashboard per dataset"""
    __tablename__ = "dashboard_package"

    id = Column(Integer, primary_key=True)
    package_id = Column(UuidType, nullable=False, unique=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500))
    embeded_url = Column(String(200))
    report_url = Column(String(200))
