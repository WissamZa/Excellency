from django.urls import path
from . import views

app_name = "service"

urlpatterns = [
    #     path("", views.sign_up_view, name="sign_up_view"),
    path('order/<lawyer_id>', views.order_form, name='order_form'),

    path('payment/<order_id>', views.payment_view, name='payment_view'),
    path('chat/', views.chat_view, name='chat_view'),
    path('orders/', views.current_orders, name='current_orders_view'),
    path('previous_orders/', views.previous_orders, name='previous_orders'),
    path('order_details/<order_id>/', views.order_details, name='order_details'),
    path('offer/add/', views.add_offer, name='add_offer'),
    path('rating/', views.rating_view, name='rating_view'),
]
