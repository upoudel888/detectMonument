from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.detect_monuments),
    path("local/",views.detect_monuments_local)
]