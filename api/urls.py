from django.urls import path
from . import views
from rest_framework_nested import routers


router = routers.DefaultRouter()

router.register("user", views.UserApiViewSet)
router.register("category", views.CategoryApiViewSet)
router.register("food-item", views.FoodItemApiViewSet)
router.register("vendor", views.VendorApiViewSet)
router.register("cart", views.CartApiViewSet)
urlpatterns = router.urls
