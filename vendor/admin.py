from django.contrib import admin
from .models import Vendor, OpeningHour, ReviewRatting


class VendorAdmin(admin.ModelAdmin):
    list_display = ("user", "vendor_name", "is_approved", "created_on")
    list_display_links = ("user", "vendor_name")
    list_editable = ("is_approved",)


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ["vendor", "day", "from_hour", "to_hour"]


admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)


admin.site.register(ReviewRatting)
