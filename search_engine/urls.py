from django.conf.urls import patterns, include, url
from django.contrib import admin
from crawler import views
from searcher import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'searcher.views.search', name='search'),
    url(r'^(?P<page>[0-9]+)/$', 'searcher.views.search', name='search'),
    url(r'^video/(?P<video_id>[-\w]+)/$', 'searcher.views.video_by_id',name='video'),
    url(r'^crawl/', 'crawler.views.crawl', name='crawl'),
)