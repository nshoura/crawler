from django.shortcuts import render, redirect
from django.http import Http404
from crawler.models import *
from searcher import views
from crawler import controller

import json
import urllib2
import logging

def crawl(request):
    # Get input
    video_url_to_crawl = request.GET.get('video_url_to_crawl', '')
    # depth implimintation
#     depth = request.GET.get('depth', '')
    video_url=video_url_to_crawl.replace('%3A',':').replace('%2F','/')

    # Check input
    # depth implimintation
#     if not depth.isdigit():
#         return render(request, 'searcher_crawler/error.html', {'error_message':'The depth must be a number!'})
#     depth=int(depth)

#     if not depth in xrange(1,26):
#         return render(request, 'searcher_crawler/error.html', {'error_message':'The depth must be between 1 and 25!'})

    if not 'youtube.com' in video_url:
        return render(request, 'searcher_crawler/error.html', {'error_message':'Please enter a YouTube video'})

    # Execute crawling algorithm
    # depth implimintation
#     return controller.crawl(request, video_url, depth)
    return controller.crawl(request, video_url, 1)


