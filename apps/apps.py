# apps/apps.py
from django.apps import AppConfig

class AppsConfig(AppConfig):
    name = 'apps'

    def ready(self):
        from .search_utils import get_search_engine
        get_search_engine()  # Build index at app startup
