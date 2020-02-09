from django import template

from WebApp.models import MemberInfo

register = template.Library()


@register.simple_tag
def getMemberFromPk(pk, attr=None):
    obj = getattr(MemberInfo.objects.get(pk=int(pk)), attr)
    return obj
