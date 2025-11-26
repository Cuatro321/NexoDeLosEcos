# codex/apps.py
from django.apps import AppConfig


class CodexConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codex"

    def ready(self):
        # Importa las señales al arrancar Django
        from . import signals  # noqa
