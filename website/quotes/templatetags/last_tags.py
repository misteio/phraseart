from quotes.models import Tag
from django import template

register = template.Library()


@register.inclusion_tag('quotes/last_tags.html')
def show_last_tags():
    tags = Tag.objects.order_by('-id')[:3]
    return {'last_tags': tags}