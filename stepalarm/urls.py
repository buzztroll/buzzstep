from django.urls import path

from . import views

urlpatterns = [
    path("", views.zeroscale, name="index"),
]
