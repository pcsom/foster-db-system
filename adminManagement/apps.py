from django.apps import AppConfig


class AdminmanagementConfig(AppConfig):
    name = 'adminManagement'

    def ready(self):
        import adminManagement.signals