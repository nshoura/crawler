from django.shortcuts import get_object_or_404, render
from crawler.models import *
from django.http import HttpResponse
from django.db.models import Q
from django.http import Http404
from itertools import chain
#https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpResponse
from django.template import RequestContext
import logging


def search(request):
    query = request.GET.get('query', '')
    if not query=="":
        results = list(chain(Video.objects.filter(Q(description__icontains = query) | Q(title__icontains = query))))[0:10]
        return render(request, 'searcher_crawler/results.html', {'results':results,'query':query})
    else:
        return render(request, 'searcher_crawler/search_crawl.html')

def video_by_id(request, video_id):
    try:
        video=Video.objects.get(video_id=video_id)
    except Video.DoesNotExist:
        raise Http404
    return render(request, 'searcher_crawler/video.html', {'video':video})

def video(request, video):
    return render(request, 'searcher_crawler/video.html', {'video':video})