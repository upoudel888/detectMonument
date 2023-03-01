from django.apps import AppConfig
from .views import get_model

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        get_model()

    