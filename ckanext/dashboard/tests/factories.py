"""Factories for creating test objects related to the dashboard extension."""

import factory
from faker import Faker
from ckan.tests import factories
from ckan import model
from ckanext.dashboard.models import DatasetDashboard

fake = Faker()


class DashboardFactory(factory.Factory):
    """Factory class for creating dashboard objects for testing."""
    
    class Meta:
        model = DatasetDashboard
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create a dashboard object and save it to the database."""
        if 'package_id' not in kwargs:
            # Create a dataset if one is not provided
            dataset = factories.Dataset()
            kwargs['package_id'] = dataset['id']
            
        if 'dashboard_type' not in kwargs:
            kwargs['dashboard_type'] = 'tableau'
            
        if 'embeded_url' not in kwargs:
            kwargs['embeded_url'] = fake.url() + '/embed?id=' + fake.lexify('????')
            
        if 'report_url' not in kwargs:
            kwargs['report_url'] = fake.url() + '/view?id=' + fake.lexify('????')
            
        dashboard = model_class(**kwargs)
        dashboard.save()
        return dashboard


def create_dashboard_for_dataset(package_id, **kwargs):
    """Helper function to create a dashboard for a specific dataset."""
    kwargs['package_id'] = package_id
    return DashboardFactory(**kwargs)


def create_tableau_dashboard(**kwargs):
    """Create a Tableau dashboard for testing."""
    if 'dashboard_type' not in kwargs:
        kwargs['dashboard_type'] = 'tableau'
    
    if 'embeded_url' not in kwargs:
        kwargs['embeded_url'] = 'https://public.tableau.com/views/TestDashboard/Sheet1?:embed=true'
    
    if 'report_url' not in kwargs:
        kwargs['report_url'] = 'https://public.tableau.com/app/profile/test/viz/TestDashboard/Sheet1'
        
    return DashboardFactory(**kwargs)


def create_powerbi_dashboard(**kwargs):
    """Create a PowerBI dashboard for testing."""
    if 'dashboard_type' not in kwargs:
        kwargs['dashboard_type'] = 'powerbi'
    
    if 'embeded_url' not in kwargs:
        kwargs['embeded_url'] = 'https://app.powerbi.com/reportEmbed?reportId=' + fake.uuid4()
    
    if 'report_url' not in kwargs:
        kwargs['report_url'] = 'https://app.powerbi.com/reports/' + fake.uuid4()
        
    return DashboardFactory(**kwargs)


def create_dashboard_with_dataset(**kwargs):
    """Create both a dataset and an associated dashboard in one go."""
    dataset = factories.Dataset()
    kwargs['package_id'] = dataset['id']
    dashboard = DashboardFactory(**kwargs)
    
    return {
        'dataset': dataset,
        'dashboard': dashboard
    }


def create_complex_dataset_with_dashboard(num_resources=2, with_owner_org=True):
    """Create a more complex dataset with resources and an organization, plus a dashboard."""
    # Create organization if requested
    org = None
    if with_owner_org:
        org = factories.Organization()
    
    # Create dataset with resources
    dataset_dict = {
        'title': fake.sentence(nb_words=4),
        'notes': fake.paragraph(),
    }
    
    if with_owner_org:
        dataset_dict['owner_org'] = org['id']
        
    dataset = factories.Dataset(**dataset_dict)
    
    # Add resources
    resources = []
    for i in range(num_resources):
        resource = factories.Resource(package_id=dataset['id'])
        resources.append(resource)
    
    # Create dashboard
    dashboard = DashboardFactory(package_id=dataset['id'])
    
    return {
        'dataset': dataset,
        'resources': resources,
        'organization': org,
        'dashboard': dashboard
    }
