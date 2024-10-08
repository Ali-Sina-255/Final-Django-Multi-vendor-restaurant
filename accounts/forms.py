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
                "form-control border w-full rounded-md py-2 px-3 text-gray-700 "
            )
        
        # Add placeholders based on the field name
            if visible.name == 'username':
                visible.field.widget.attrs.update({'placeholder': 'Enter your username'})
            elif visible.name == 'email':
                visible.field.widget.attrs.update({'placeholder': 'Enter your email address'})
            elif visible.name == 'password':
                visible.field.widget.attrs.update({'placeholder': 'Enter your password'})
            
            elif visible.name == 'first_name':
                visible.field.widget.attrs.update(
                    {'placeholder':'Enter your Fist name'}
                )
            
            elif visible.name == 'last_name':
                visible.field.widget.attrs.update(
                    {'placeholder':'Enter your last name'}
                )
            elif visible.name == 'confirm_password':
                 visible.field.widget.attrs.update(
                    {'placeholder':'Enter your Confirm password.'}
                )
                 
            elif visible.name == 'confirm_password':
                 visible.field.widget.attrs.update(
                    {'placeholder':'Enter your Confirm password.'}
                )
                 
            elif visible.name == 'vendor_name':
                visible.field.widget.attrs.update(
                    {'placeholder':'Enter your restaurant name'}
                )
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Start typing", "required": "required"}
        )
    )
    profile_pic = forms.FileField(widget=forms.FileInput(attrs={'class':'bg-blue-500 text-white rounded-md py-4 px-4'}))
    cover_pic = forms.FileField(widget=forms.FileInput(attrs={'class':'bg-blue-500 text-white rounded-md py-4 px-4'}))
    # profile_pic = forms.FileField(
    #     widget=forms.FileInput(attrs={"class": "  bg-blue-500 text-white rounded-md py-4 px-4"})
    # )
    # cover_pic = forms.FileField(
    #     widget=forms.FileInput(attrs={"class": "bg-blue-500 text-white rounded-md py-4 px-4"})
    # )

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
                "px-4 py-2 border border-gray-300 rounded-lg w-full text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            )


class UserInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number"]

    def __init__(self, *args, **kwargs):
        super(UserInForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = (
                "px-4 py-2 border border-gray-300 rounded-lg w-full text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            )