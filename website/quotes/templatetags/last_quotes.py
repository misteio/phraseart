from quotes.models import Quote
from django import template

register = template.Library()


@register.inclusion_tag('quotes/last_quotes.html')
def show_last_quotes():
    quotes = Quote.objects.filter(explicit_text=False).order_by('-id')[:3]
    return {'last_quotes': quotes}