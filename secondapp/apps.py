from django.apps import AppConfig

class SecondappConfig(AppConfig):
    name = 'secondapp'

    def ready(self):
        from . import signals
