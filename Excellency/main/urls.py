from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.index_view, name="index_view"),
    path("lawyers", views.lawyers_view, name="lawyers_view"),
    path("contactus", views.contactus_view, name="contactus_view"),
    path("contact_messages", views.contact_messages, name="contact_messages"),
    path("admin_viwe", views.admin_viwe, name="admin_viwe"),
    path('lawyer_details/<user_id>', views.lawyer_details_view, name='lawyer_details'),
    path('post/', views.post_list, name='post_list'),
    path("verification/<user_id>/",views.verification,name="verification"),
]
