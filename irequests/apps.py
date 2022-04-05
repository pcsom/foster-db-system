from django.apps import AppConfig


class IrequestsConfig(AppConfig):
    name = 'irequests'

    def ready(self):
        import irequests.signals