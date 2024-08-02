from django.core.exceptions import ValidationError
import os


def allow_only_images_validator(value):
    extensions = os.path.split(value.name)[1]
    valid_extension = ["jpg", "png", "jpeg"]
    if not extensions.lower() in valid_extension:
        raise ValidationError("this extension is not suported")


def allow_only_images_validator(value):
    extensions = os.path.split(value.name)[1]
    valid_extension = ["jpg", "png", "jpeg"]
    if not extensions.lower() in valid_extension:
        raise ValidationError(
            "Unsupported file extension.Allowed Extension" + str(valid_extension)
        )
