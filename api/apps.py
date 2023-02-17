from django.apps import AppConfig
import torch


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    model = torch.hub.load('api\yolov5', 'custom', path = 'api\yolov5\weights\\best.pt', source = 'local',device='cpu')
