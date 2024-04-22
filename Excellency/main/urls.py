from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.index_view, name="index_view"),
    path("lawyers", views.lawyers_view, name="lawyers_view"),
    path("contactus", views.contactus_view, name="contactus_view"),
]
