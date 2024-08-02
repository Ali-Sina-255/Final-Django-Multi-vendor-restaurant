from django.urls import path
from . import views

urlpatterns = [path("", views.user_registration_view, name="register")]
