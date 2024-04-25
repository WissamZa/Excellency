from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("sign_up/", views.sign_up_view, name="sign_up_view"),
    path("user/", views.user_profile_view, name="user_profile_view"),
    #     path("user/<user_name>/",views.user_profile_view, name="user_profile_view"),
    path("profile/<user_name>/update/",
         views.update_profile_view, name="update_profile_view"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("lawyer/<user_id>/profile/",
         views.profile_view, name="profile_view"),
    #     path("<username>/cart/", views.cart_view, name="cart_view"),
    #     path(f"<username>/cart/delete/<cart_id>/", views.delete_product_view,name="delete_product_view"),
    path("account_balance/", views.account_balance, name="account_balance"),
]
