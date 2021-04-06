# flake8: noqa
from django.apps import AppConfig


class ModsConfig(AppConfig):
    name = 'mods'

    def ready(self):
        import mods.signals
