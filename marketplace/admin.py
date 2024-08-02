from django.contrib import admin
from .models import Cart, Tax


class TaxAdmin(admin.ModelAdmin):
    list_display = ["tax_type", "is_active"]


class CartAdminModel(admin.ModelAdmin):
    list_display = ["user", "food_item", "quantity", "updated_at"]


admin.site.register(Cart, CartAdminModel)
admin.site.register(Tax, TaxAdmin)
