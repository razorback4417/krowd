from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("donate/", views.donate, name="donate"),
    path("starp/", views.starp, name="starp"),
    path("createProject/", views.createProject, name="createProject")
]