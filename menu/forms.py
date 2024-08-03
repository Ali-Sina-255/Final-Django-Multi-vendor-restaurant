from django import forms
from .models import Category, FootItem
from accounts.validators import allow_only_images_validator


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "description"]

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields["category_name"].widget.attrs.update(
            {
                "class": "appearance-none border rounded-md shadow-md w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "placeholder": "Enter category title",
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "appearance-none border rounded-md shadow-md w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "placeholder": "Enter category description",
                "rows": 6,
            }
        )


class FoodItemForm(forms.ModelForm):
    image = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info w-100"})
    )

    class Meta:
        model = FootItem
        fields = [
            "category",
            "food_title",
            "description",
            "price",
            "image",
            "is_available",
        ]

    def __init__(self, *args, **kwargs):
        super(FoodItemForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            # Apply Tailwind CSS classes to all fields except 'image'
            if field != "image":
                self.fields[field].widget.attrs.update(
                    {
                        "class": "appearance-none border rounded-md w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    }
                )

        # Customize 'image' field separately
        self.fields["image"].widget.attrs.update({"class": "btn btn-info w-100"})
