from django.urls import path
from . import views

app_name = "service"

urlpatterns = [
    #     path("", views.sign_up_view, name="sign_up_view"),
    path('order/', views.order_form, name='order_form'),
    path('payment/', views.payment_view, name='payment_view'),
    path('chat/', views.chat_view, name='chat_view'),
    
]
