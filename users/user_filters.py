from django import template

from django import template

register = template.Library()

@register.filter
def my_filter(value):
    # your filter code here
    return value

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])

