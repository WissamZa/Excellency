from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.index_view, name="index_view"),
    path("lawyers", views.lawyers_view, name="lawyers_view"),
    path("contactus", views.contactus_view, name="contactus_view"),
    path("contact_messages", views.contact_messages, name="contact_messages"),
    path("admin_view", views.admin_view, name="admin_view"),
    path('lawyer_details/<user_id>', views.lawyer_details_view, name='lawyer_details'),
    path('post/', views.post_list, name='post_list'),
    path("verification/<user_id>/", views.verification, name="verification"),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/', views.post_view, name='post_view'),

    path('post/<int:post_id>/bookmark/', views.bookmark_post, name='bookmark_post'),
    path('contact/success/', views.contact_success, name='contact_success'),

]
