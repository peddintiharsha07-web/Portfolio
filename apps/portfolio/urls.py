from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/submit/", views.contact_submit, name="contact_submit"),
    path("project/<slug:slug>/", views.project_detail, name="project_detail"),
]
