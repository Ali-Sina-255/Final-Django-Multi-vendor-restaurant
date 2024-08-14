import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_vendor_name(value):
    if not re.match(r'^[A-Za-z]+$', value):
        raise ValidationError(_('Vendor name must only contain alphabetic characters without spaces.'))
