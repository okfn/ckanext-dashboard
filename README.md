[![Tests](https://github.com//ckanext-dashboard/workflows/Tests/badge.svg?branch=main)](https://github.com//ckanext-dashboard/actions)

# ckanext-dashboard

**TODO:** Put a description of your extension here:  What does it do? What features does it have? Consider including some screenshots or embedding a video!


## Requirements

**TODO:** For example, you might want to mention here which versions of CKAN this
extension works with.

If your extension works across different versions you can add the following table:

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | not tested    |

Suggested values:

* "yes"
* "not tested" - I can't think of a reason why it wouldn't work
* "not yet" - there is an intention to get it working
* "no"


## Installation

**TODO:** Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-dashboard:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com//ckanext-dashboard.git
    cd ckanext-dashboard
    pip install -e .
	pip install -r requirements.txt

3. Add `dashboard` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

None at present

**TODO:** Document any optional config settings here. For example:

	# The minimum number of hours to wait before re-checking a resource
	# (optional, default: 24).
	ckanext.dashboard.some_setting = some_default_value


## Developer installation

To install ckanext-dashboard for development, activate your CKAN virtualenv and
do:

    git clone https://github.com//ckanext-dashboard.git
    cd ckanext-dashboard
    pip install -e .
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-dashboard

If ckanext-dashboard should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `pyproject.toml` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python -m build && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)

## 🛠️ Troubleshooting

See [Troubleshooting procedure](/docs/Troubleshooting.md)


## Configuration

This extension allows customization of the dashboard title displayed on dataset pages.

### `ckanext.bcie.dashboard_title`

- **Type:** `string`
- **Default:** `"Dashboard"`
- **Description:** Sets the title that appears above the embedded dashboard in the dataset detail page.
- **Usage:** You can change this setting in the CKAN configuration file (`.ini`), or leave it blank to hide the title entirely.

#### Example

To customize the title:

```ini
ckanext.bcie.dashboard_title = Project Monitoring
```

To hide the title completely:

```ini
ckanext.bcie.dashboard_title = 
```

> Note: This setting is read directly from the CKAN configuration file. If you wish to expose it in the sysadmin UI (`/admin/config`), you will need to register a config validator in the plugin.
