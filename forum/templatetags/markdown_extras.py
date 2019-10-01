from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):

    import re
    import html
    value = html.unescape(value)
    text = re.sub(re.compile('<.*?>'), "", value)
    return md.markdown(text, extensions=['markdown.extensions.fenced_code'])
