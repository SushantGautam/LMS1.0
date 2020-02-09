from django import template

from WebApp.models import MemberInfo

register = template.Library()


@register.simple_tag
def get_obj(pk):
    obj = MemberInfo.objects.get(pk=int(pk))
    return obj
