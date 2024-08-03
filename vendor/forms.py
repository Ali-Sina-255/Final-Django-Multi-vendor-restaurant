from django import forms
from .models import Vendor, OpeningHour, ReviewRatting
from accounts.forms import allow_only_images_validator


class VendorRegisterForm(forms.ModelForm):
    vendor_licenses = forms.FileField(
        widget=forms.FileInput(attrs={"class": "bnt btn-info"})
    )

    class Meta:
        model = Vendor
        fields = ["vendor_name", "vendor_licenses"]

    def __init__(self, *args, **kwargs):
        super(VendorRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = (
                "form-control  w-full border rounded-lg py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            )


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ["day", "from_hour", "to_hour", "is_closed"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRatting
        fields = ["subject", "review", "ratting"]
