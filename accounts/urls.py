from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.my_account_view),
    path("register/", views.user_registration, name="register"),
    path("register_vendor/", views.register_vendor, name="register_vendor"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "customer_dashboard/", views.customer_dashboard_view, name="customer_dashboard"
    ),
    path("vendor_dashboard/", views.vendor_dashboard_view, name="vendor_dashboard"),
    path("my_account/", views.my_account_view, name="my_account"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("forgot_password/", views.forgot_password_view, name="forgot_password"),
    path(
        "reset_password_validate/<uidb64>/<token>/",
        views.reset_password_validate_view,
        name="reset_password_validate",
    ),
    path("rest_password", views.reset_password_view, name="reset_password"),
    path("vendor/", include("vendor.urls")),
]
