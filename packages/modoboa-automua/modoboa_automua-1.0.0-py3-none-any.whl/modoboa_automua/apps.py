from django.apps import AppConfig


class ModoboaAutoMUAConfig(AppConfig):
    name = 'modoboa_automua'

    def ready(self):
        from . import handlers  # noqa: F401
