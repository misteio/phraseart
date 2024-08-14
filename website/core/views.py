from django.shortcuts import render
from django.http import HttpResponse
from quotes.models import Quote
import os
from django.template import RequestContext
from django.conf import settings

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
