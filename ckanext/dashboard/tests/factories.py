import factory
from ckan import model
from ckantoolkit.tests import factories
from ckanext.dashboard.models import DatasetDashboard


class DashboardFactory(factory.Factory):
    class Meta:
        model = DatasetDashboard

    packageid = factory.LazyAttribute(lambda obj: factories.Dataset()['id'])
    dashboard_type = factory.Iterator(['tableau', 'powerbi'])
    embeded_url = factory.Sequence(lambda n: "https://embed.com/embed-{0:05d}.html".format(n))
    report_url = factory.Sequence(lambda n: "https://report.com/embed-{0:05d}.html".format(n))

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        obj = target_class(**kwargs)
        model.Session.add(obj)
        model.Session.commit()
        model.Session.remove()

        return obj
