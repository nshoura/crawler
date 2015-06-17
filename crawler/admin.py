from django.contrib import admin
from crawler.models import *

class VideoAdmin(admin.ModelAdmin):
    list_display = ('video_id', 'title')
    fields = ['title','description','video_id','embed_html','owner_name','owner_id','owner_url','thumbnail_url','related','views_total','video_url']

admin.site.register(Video, VideoAdmin)