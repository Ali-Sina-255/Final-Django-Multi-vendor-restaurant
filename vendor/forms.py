from django import forms
from .models import Vendor, OpeningHour, ReviewRatting
from accounts.forms import allow_only_images_validator

class VendorRegisterForm(forms.ModelForm):
    vendor_licenses = forms.FileField(
        widget=forms.FileInput(attrs={"class": "border-0 pb-5 rounded-md"})
    )

    class Meta:
        model = Vendor
        fields = ["vendor_name", "vendor_licenses"]

    def __init__(self, *args, **kwargs):
        super(VendorRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = (
                "form-control border w-full rounded-md py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
            )
            # Add the class pb-5 to the label
            if visible.label:
                visible.label = f'<label class="pb-5">{visible.label}</label>'


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ["day", "from_hour", "to_hour", "is_closed"]

    def __init__(self, *args, **kwargs):
        super(OpeningHoursForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = (
                "form-control border w-full rounded-md py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
            )
            # Add the class pb-5 to the label
            if visible.label:
                visible.label = f'<label class="pb-5">{visible.label}</label>'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRatting
        fields = ["subject", "review", "ratting"]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = (
                "form-control border w-full rounded-md py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
            )
            # Add the class pb-5 to the label
            if visible.label:
                visible.label = f'<label class="pb-5">{visible.label}</label>'
