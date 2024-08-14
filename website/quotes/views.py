from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from .models import Quote,Tag, Author


# Create your views here.
# @cache_page(60 * 90)
@require_http_methods(["GET"])
def index(request):
    quotes = Quote.objects.all().order_by('-created_at')[:10]
    return render(request, 'index.html', {'quotes': quotes})


@require_http_methods(["GET"])
def quote(request, slug):
    queryset = Quote.random_objects
    random_quotes = queryset.random(6).prefetch_related('tags').select_related('author')
    quote = get_object_or_404(Quote, slug=slug)

    previous_quote = (Quote.objects
                      .filter(id__lt=quote.id)
                      .exclude(id=quote.id)
                      .order_by('-id')
                      .first())
    next_quote = (Quote.objects
                  .filter(id__gt=quote.id)
                  .exclude(id=quote.id)
                  .order_by('id')
                  .first())

    return render(request, 'single_quote.html',
                  {'quote': quote, 'random_quotes': random_quotes[1:6], 'next_quote': next_quote,
                   'previous_quote': previous_quote, 'random_quote': random_quotes[0]})


@require_http_methods(["GET", "POST"])
def tag_list(request, tag_slug, template='category_list.html', page_template='quote_list_page.html'):
    tag = Tag.objects.filter(slug__exact=tag_slug).first()
    skip = 0
    context = {
        'quotes': get_list_or_404(Quote.objects.filter(tags__slug__exact=tag_slug).order_by('-created_at')[skip:10+skip]),
        'tag': tag,
        'page_template': 'page_template',
        'title' : "Citations pour le mot clé '" + tag.name + "'"
    }

    return render(request, template, context)


@require_http_methods(["GET", "POST"])
def author_list(request, author_slug, template='category_list.html', page_template='quote_list_page.html'):
    author = Author.objects.filter(slug__exact=author_slug).first()
    skip = 0
    context = {
        'quotes': get_list_or_404(Quote.objects.filter(author__slug__exact=author_slug).order_by('-created_at')[skip:10+skip]),
        'author': author,
        'page_template': 'page_template',
        'title': "Auteur '" + author.name + "'"
    }

    return render(request, template, context)


@require_http_methods(["GET", "POST"])
def all_quotes(request, template='category_list.html', page_template='quote_list_page.html'):
    skip = 0
    context = {
        'quotes': get_list_or_404(Quote.objects.order_by('-created_at')[skip:10+skip]),
        'category': None,
        'page_template': 'page_template',
        'title': "Toutes les citations"
    }

    return render(request, template, context)


@require_http_methods(["GET"])
def search(request):
    params = {"hitsPerPage": 100, 'similarQuery': request.GET.getlist('q')}

    quote_ids = []

    quotes = list(Quote.objects.filter(pk__in=quote_ids))
    quotes.sort(key=lambda t: quote_ids.index(t.pk))
    return render(request, 'search.html', {'quotes': quotes, 'search': request.GET.get('q'), 'count': response['nbHits']})
