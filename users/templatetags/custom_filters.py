# myapp/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def to(start, end):
    """Return a range from start to end inclusive."""
    try:
        start_int = int(start)
        end_int = int(end)
        return range(start_int, end_int + 1)
    except Exception:
        return []

@register.filter
def get_range(value):
    """Return a range from 0 to value (exclusive)"""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)