from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from ckan.model.types import UuidType
from ckan import model


Base = declarative_base()


class DatasetDashboard(Base):
    """Data model for storing the configuration of a dashboard per dataset"""
    __tablename__ = "dashboard_package"

    id = Column(Integer, primary_key=True)
    package_id = Column(UuidType, nullable=False, unique=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500))
    dashboard_type = Column(String(50))
    embeded_url = Column(String(200))
    report_url = Column(String(200))

    def dictize(self):
        return {
            'id': self.id,
            'package_id': str(self.package_id),
            'title': self.title,
            'description': self.description,
            'dashboard_type': self.dashboard_type,
            'embeded_url': self.embeded_url,
            'report_url': self.report_url
        }

    def save(self):
        model.Session.add(self)
        model.Session.commit()
        model.Session.refresh(self)
        return self
