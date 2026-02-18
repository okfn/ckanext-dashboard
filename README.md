
# ckanext-dashboard

A CKAN extension that allows embedding external dashboards and visualizations from Business Intelligence tools like **Tableau** and **PowerBI** directly into CKAN dataset pages.

## Features

- **Embed Interactive Dashboards**: Display Tableau, PowerBI, or other BI tool visualizations within dataset pages
- **Link to Full Reports**: Add optional links to the complete dashboard/report
- **Admin Controlled**: Only sysadmins can create, edit, and delete dashboard configurations
- **Internationalized**: Built-in support for English and Spanish
- **Customizable Titles**: Configure or hide dashboard section titles via configuration
- **Multiple Dashboard Types**: Support for various BI platforms (Tableau, PowerBI)

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | yes           |
| 2.10            | yes           |
| 2.11            | yes           |

**Python compatibility**: 3.8, 3.9, 3.10


## Installation

To install ckanext-dashboard:

1. Activate your CKAN virtual environment, for example:
   ```bash
   . /usr/lib/ckan/default/bin/activate
   ```

2. Clone the source and install it on the virtualenv:
   ```bash
   git clone https://github.com//ckanext-dashboard.git
   cd ckanext-dashboard
   pip install -e .
   pip install -r requirements.txt
   ```

3. Add `dashboard` to the `ckan.plugins` setting in your CKAN config file (by default the config file is located at `/etc/ckan/default/ckan.ini`).

4. Initialize the database tables:
   ```bash
   ckan db upgrade -p dashboard
   ```

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:
   ```bash
   sudo service apache2 reload
   ```


## Config settings

### `ckanext.dashboard.title`

- **Type:** `string`
- **Default:** `"Dashboard"`
- **Description:** Sets the title that appears above the embedded dashboard in the dataset detail page.
- **Usage:** You can change this setting in the CKAN configuration file (`.ini`), or leave it blank to hide the title entirely.

#### Example

To customize the title:
```ini
ckanext.dashboard.title = Project Monitoring
```

To hide the title completely:
```ini
ckanext.dashboard.title = 
```

> **Note**: This setting is read directly from the CKAN configuration file.


## Usage

### Creating a Dashboard for a Dataset

1. Navigate to a dataset page as a sysadmin user
2. Click on the "Dashboard" tab or navigate to `/dataset/dashboard/{package_id}`
3. Fill in the form:
   - **Dashboard Type**: Select the type of dashboard (e.g., `tableau`, `powerbi`)
   - **Embedded URL**: The iframe URL for embedding the dashboard
   - **Report URL**: (Optional) Link to the full dashboard/report
   - **Report Title**: (Optional) Custom text for the report link (default: "View full report")
4. Click "Save"

The dashboard will now be displayed on the dataset page below the description.

> **Note**: Only users with edit permissions on the dataset can create or modify dashboards. Viewing dashboards requires read access to the dataset.

### API Actions

The extension provides the following API actions:

- `dataset_dashboard_show`: Get dashboard configuration for a dataset
- `dataset_dashboard_create`: Create a new dashboard configuration
- `dataset_dashboard_update`: Update an existing dashboard configuration
- `dataset_dashboard_delete`: Delete a dashboard configuration

**Example**:
```python
import ckan.plugins.toolkit as toolkit

# Show dashboard for a dataset
dashboard = toolkit.get_action('dataset_dashboard_show')(
    context, 
    {'pkg_id': 'my-dataset-id'}
)

# Create a dashboard
new_dashboard = toolkit.get_action('dataset_dashboard_create')(
    context,
    {
        'package_id': 'my-dataset-id',
        'dashboard_type': 'tableau',
        'embeded_url': 'https://tableau.example.com/embed/...',
        'report_url': 'https://tableau.example.com/full-report',
        'report_title': 'View Full Report'
    }
)
```

## Developer installation

To install ckanext-dashboard for development, activate your CKAN virtualenv and do:

```bash
git clone https://github.com//ckanext-dashboard.git
cd ckanext-dashboard
pip install -e .
pip install -r dev-requirements.txt
```

## Tests

To run the tests, do:

```bash
pytest --ckan-ini=test.ini
```

To run tests with coverage:

```bash
pytest --ckan-ini=test.ini --cov=ckanext.dashboard --disable-warnings ckanext/dashboard
```


## Releasing a new version of ckanext-dashboard

If ckanext-dashboard should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `pyproject.toml` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:
   ```bash
   pip install --upgrade setuptools wheel twine
   ```

3. Create a source and binary distributions of the new version:
   ```bash
   python -m build && twine check dist/*
   ```
   Fix any errors you get.

4. Upload the source distribution to PyPI:
   ```bash
   twine upload dist/*
   ```

5. Commit any outstanding changes:
   ```bash
   git commit -a
   git push
   ```

6. Tag the new release of the project on GitHub with the version number from the `pyproject.toml` file. For example if the version number in `pyproject.toml` is 0.1.4 then do:
   ```bash
   git tag 0.1.4
   git push --tags
   ```

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)

## Troubleshooting

See [Troubleshooting procedure](/docs/Troubleshooting.md) for common issues including:
- iframe overflow problems
- Report sizing in Power BI
- Embedding configuration for Tableau
