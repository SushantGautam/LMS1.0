from django.apps import AppConfig


class WebAppConfig(AppConfig):
    name = 'WebApp'

    def ready(self):
        import WebApp.signals
