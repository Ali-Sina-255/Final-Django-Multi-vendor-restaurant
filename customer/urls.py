from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.customer_profile_view, name="c_profile"),
    path("my_order/", views.my_orders_view, name="my_order"),
    path(
        "order_detail/<int:order_number>/", views.order_detail_view, name="order_detail"
    ),
]
