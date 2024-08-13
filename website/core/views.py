from django.shortcuts import render
from django.http import HttpResponse
from quotes.models import Quote
import os
from django.template import RequestContext
from django.conf import settings

# Create your views here.
def image_download(request):
    quote_slug = request.GET['quote_slug']
    image_format = request.GET['format']
    quote = Quote.objects.filter(slug=quote_slug).first()

    fl_path = settings.MEDIA_ROOT + getattr(quote, image_format)

    with open(fl_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="image/png")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(fl_path)
        return response


def handler404(request, *args, **argv):
    response = render('404.html', {},
                      context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render('500.html', {},
                      context_instance=RequestContext(request))
    response.status_code = 500
    return response
