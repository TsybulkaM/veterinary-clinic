from django.apps import AppConfig


class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vetclinic'

    def ready(self):
        import vetclinic.signals
