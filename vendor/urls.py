from django.urls import path
from accounts import views as account_views
from . import views


urlpatterns = [
    path("", account_views.vendor_dashboard_view, name="vendor"),
    path("profile/", views.vendor_profile, name="vendor_profile"),
    
    path("menu_builder/add_category/", views.add_category, name="add_category"),
    path("menu_builder/", views.menu_builder, name="menu_builder"),
    path(
        "menu_builder/category/<int:pk>/",
        views.food_items_by_category,
        name="food_items_by_category",
    ),

    path("menu_builder/edit/<int:pk>/", views.edit_category, name="edit_category"),
    path(
        "delete_category/<int:pk>/", views.delete_category, name="delete_category"
    ),
    # CRUD Food Items
    path("menu_builder/food/add/", views.add_food_view, name="add_food"),
    path("menu_builder/food/edit/<int:pk>/", views.edit_food_view, name="edit_food"),
    path(
        "menu_builder/food/delete/<int:pk>/", views.delete_food_view, name="delete_food"
    ),
    # OPENING_HOURS
    path("opening_hours/", views.opening_hours_view, name="opening_hours"),
   path("opening_hours/add/", views.add_opening_hour_view, name="add_opening"),
    path(
        "opening_hours/remove/<int:pk>/",
        views.remove_opening_hour_view,
        name="remove_hour",
    ),
    path(
        "vendor_order_detail/<int:order_number>/",
        views.vendor_order_details_view,
        name="vendor_order_detail",
    ),
    path("my_order_vendor/", views.my_order_view, name="my_order_vendor"),
]
