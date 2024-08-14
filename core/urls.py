from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as marketplace_view

from django.shortcuts import render
from vendor.models import Vendor

def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:10]
    context = {"vendors": vendors}
    return render(request, "index.html", context)


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("cart/", marketplace_view.cart_view, name="cart"),
    path("search/", marketplace_view.search_view, name="search"),
    path("checkout/", marketplace_view.checkout_view, name="checkout"),
    path("marketplace/", include("marketplace.urls")),
    path("customer/", include("customer.urls")),
    path("order/", include("orders.urls")),
    path("api/", include("api.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "FoodOnline Market Place"
admin.site.site_title = "FoodOnline Market Place"
admin.site.index_title = "FoodOnline Market Place"