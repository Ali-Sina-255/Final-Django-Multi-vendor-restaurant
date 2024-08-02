from django.urls import path
from . import views

urlpatterns = [path("", views.FoodItemApiListView.as_view(), name="food")]
