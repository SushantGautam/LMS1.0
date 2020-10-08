from django import template
from django.template.defaulttags import register
register = template.Library()

@register.simple_tag
def define(val=None):
  return val

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)