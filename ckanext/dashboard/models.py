from sqlalchemy import Column, Integer, String

from ckan import model
from ckan.model.types import UuidType
from ckan.plugins import toolkit


class DatasetDashboard(toolkit.BaseModel):
    """Data model for storing the configuration of a dashboard per dataset"""
    __tablename__ = "dashboard_dashboard"

    id = Column(Integer, primary_key=True)
    package_id = Column(UuidType, nullable=False, unique=True)
    dashboard_type = Column(String(20))
    embeded_url = Column(String(2000))
    report_url = Column(String(2000))

    def dictize(self):
        return {
            'id': self.id,
            'package_id': str(self.package_id),
            'dashboard_type': self.dashboard_type,
            'embeded_url': self.embeded_url,
            'report_url': self.report_url
        }

    def save(self):
        model.Session.add(self)
        model.Session.commit()
        model.Session.refresh(self)
        return self
