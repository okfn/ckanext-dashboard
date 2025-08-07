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
    # We want to allow an optional secondary button/link with a different URL and a custom title
    secondary_button_url = Column(String(2000), nullable=True)
    secondary_button_title = Column(String(200), nullable=True)

    def dictize(self):
        return {
            'id': self.id,
            'package_id': str(self.package_id),
            'dashboard_type': self.dashboard_type,
            'embeded_url': self.embeded_url,
            'report_url': self.report_url,
            'secondary_button_url': self.secondary_button_url,
            'secondary_button_title': self.secondary_button_title,
        }

    def save(self):
        model.Session.add(self)
        model.Session.commit()
        model.Session.refresh(self)
        return self
