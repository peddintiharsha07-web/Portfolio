from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("project/<int:pk>/", views.project_detail, name="project_detail"),
    path("set-color/", views.set_color, name="set_color"),
]
