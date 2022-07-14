from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def round_down(value, size=1):
    size = Decimal(size)
    return (Decimal(value)//size) * size

@register.filter
def round_down_int(value, size=1):
    size = int(size)
    return (value//size) * size