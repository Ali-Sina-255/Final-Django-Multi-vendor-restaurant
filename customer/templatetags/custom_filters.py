# myapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_grand_total(order, vendor):
    return order.get_total_by_vendor()['grand_total']
