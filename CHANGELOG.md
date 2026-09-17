# Changelog

## 0.1.5 - 2026-09-16

### Added

- CKAN 2.12 compatibility and CI coverage while retaining CKAN 2.11 test coverage.
- Configuration declaration for `ckanext.dashboard.title`.
- CSRF tokens in dashboard create, update, and delete forms.

### Changed

- Document support for CKAN 2.12 and Python 3.11.
- End CKAN 2.10 support after version 0.1.4.
- Use `toolkit.current_user` instead of the legacy request context proxy.
