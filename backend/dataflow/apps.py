import atexit

from django.apps import AppConfig


class DataflowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dataflow'
    verbose_name = 'DataFlow'

    _cleanup_registered = False

    def ready(self):
        if self.__class__._cleanup_registered:
            return

        from code_server.manager import manager as code_server_manager

        atexit.register(code_server_manager.stop_all)
        self.__class__._cleanup_registered = True
