from django.apps import AppConfig


class UaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "UA"
    def ready(self):
        from . import signals  # noqa
