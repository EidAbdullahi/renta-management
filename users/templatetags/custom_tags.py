# users/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def get_range(value):
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)

@register.filter
def to(start, end):
    try:
        start_int = int(start)
        end_int = int(end)
        return range(start_int, end_int + 1)
    except Exception:
        return []
