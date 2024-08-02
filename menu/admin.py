from django.contrib import admin
from .models import Category, FootItem


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)}
    list_display = ["category_name", "vendor", "updated_at"]
    search_fields = ["category_name", "vendor__vendor_name"]


admin.site.register(Category, CategoryAdmin)


class FootItemAdmin(admin.ModelAdmin):
    list_display = [
        "food_title",
        "category",
        "vendor",
        "price",
        "is_available",
        "updated_at",
    ]
    search_fields = [
        "food_title",
        "category__category_name",
        "vendor__vendor_name",
        "price",
    ]
    list_filter = ["is_available"]


admin.site.register(FootItem, FootItemAdmin)
