from django.urls import path
from . import views

urlpatterns = [
    path("", views.generate_font, name="generate_font"),
    path("sample/", views.download_sample, name="download_sample"),
]
