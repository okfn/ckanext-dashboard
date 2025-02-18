"""
Connect to the dashboard API (through a proxy server if required)
"""
import logging

from ckan.plugins.toolkit import config


log = logging.getLogger(__name__)


def get_config():
    """ Get configuration values for dashboard and proxy"""
    log.debug("Getting dashboard configuration values")
    cfg = {
        'dashboard_url': config.get("ckanext.dashboard.instance.url").rstrip('/'),
        'dashboard_user': config.get("ckanext.dashboard.instance.user"),
        'dashboard_pass': config.get("ckanext.dashboard.instance.pass"),
        'dashboard_provider': config.get("ckanext.dashboard.instance.provider", "db"),
        'dashboard_refresh': config.get("ckanext.dashboard.instance.refresh", "true")
    }

    log.info(f'Configuration values: dashboard: {cfg["dashboard_url"]}, Proxy: {cfg.get("proxy_url")}')

    return cfg
