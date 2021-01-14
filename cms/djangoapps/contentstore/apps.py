"""
Contentstore Application Configuration

Above-modulestore level signal handlers are connected here.
"""


from django.apps import AppConfig
from django.conf import settings
from edx_proctoring.runtime import set_runtime_service


class ContentstoreConfig(AppConfig):
    """
    Application Configuration for Contentstore.
    """
    name = u'cms.djangoapps.contentstore'

    def ready(self):
        """
        Connect handlers to signals.
        """
        # Can't import models at module level in AppConfigs, and models get
        # included from the signal handlers
        from .signals import handlers  # pylint: disable=unused-import

        if settings.FEATURES.get('ENABLE_SPECIAL_EXAMS'):
            from .services import ContentstoreService
            set_runtime_service('contentstore', ContentstoreService())
