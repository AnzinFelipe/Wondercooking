import re
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()

def criar_hashtag_link(tag):
    url="/tags/{}/".format(tag)
    return '<a href="{}">#{}</a>'.format(url,tag)

@register.filter(name='link_hashtags')
def link_hashtags(texto):
    return mark_safe(re.sub(r'#(\w+)', lambda m: criar_hashtag_link(m.group(1)), escape(texto)))
