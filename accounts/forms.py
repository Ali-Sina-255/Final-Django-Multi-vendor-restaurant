from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import User, UserProfile
from .validators import allow_only_images_validator


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
        ]

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = (
                "form-control border rounded-md py-4 px-3 text-gray-700 "
            )
            visible.label_tag(attrs={'class': 'pb-5'})


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Start typing", "required": "required"}
        )
    )
    profile_pic = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"})
    )
    cover_pic = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info"}))

    class Meta:
        model = UserProfile
        fields = [
            "profile_pic",
            "cover_pic",
            "address",
            "state",
            "city",
            "latitude",
            "longitude",
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field in ["latitude", "longitude"]:
                self.fields[field].widget.attrs["readonly"] = "readonly"

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = (
                "px-5 form-control border rounded-lg py-2 px-3 w-full text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            )


class UserInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number"]
