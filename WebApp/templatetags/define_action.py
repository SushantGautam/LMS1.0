from django import template
register = template.Library()

@register.simple_tag
def define(val=None):
  return val

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)