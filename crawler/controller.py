from django.shortcuts import render, redirect
from django.http import Http404
from crawler.models import *
from searcher import views

import json
import urllib2
import logging

def crawl(request, video_url, depth):

    # Execute crawling algorithm
    video = parse_video(video_url)
    crawl_video(video, depth)
    return views.video(request, video)

def parse_video(video_url):
    try:
        video=Video.objects.get(video_id = video_url.split('=')[1].split('&')[0])
    except Video.DoesNotExist:
        video=Video(video_id = video_url.split('=')[1].split('&')[0])
        video.video_api_url = 'https://www.googleapis.com/youtube/v3/videos?key=AIzaSyBp-A5_icKU-m0KuFLf0wOvQwbayFC-JEM&id='+video.video_id
        video.video_url = "http://www.youtube.com/watch?v="+video.video_id
        video_info =json.loads(urllib2.urlopen(video.video_api_url+'&part=snippet,statistics,player&fields=items(id,snippet/title,snippet/description,snippet/thumbnails/default/url,snippet/channelTitle,snippet/channelId,snippet/tags,statistics/viewCount,player/embedHtml)').read())
        video.description = video_info['items'][0]['snippet']['description']
        video.embed_html = (video_info['items'][0]['player']['embedHtml'])[0:-2]+"></iframe>"
        video.owner_id=video_info['items'][0]['snippet']['channelId']
        video.owner_name=video_info['items'][0]['snippet']['channelTitle']
        video.owner_url='http://www.youtube.com/channel/'+video_info['items'][0]['snippet']['channelId']
        video.thumbnail_url = video_info['items'][0]['snippet']['thumbnails']['default']['url']
        video.title = video_info['items'][0]['snippet']['title']
        video.views_total = video_info['items'][0]['statistics']['viewCount']
        video.save()
    return video

def get_related_videos_urls(video):
    related_videos_urls = []
    related_videos_data = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&key=AIzaSyBp-A5_icKU-m0KuFLf0wOvQwbayFC-JEM&relatedToVideoId="+video.video_id).read())['items']
    for related_video_data in related_videos_data:
            related_videos_urls.append("http://www.youtube.com/watch?v="+related_video_data['id']['videoId'])
    return related_videos_urls

def add_related_videos(video):
    related_videos_urls = get_related_videos_urls(video)
    for related_video_url in related_videos_urls:
        related_video = parse_video(related_video_url)
        video.related.add(related_video)

def crawl_video(video, depth):
    add_related_videos(video)
    if depth > 0:
        depth -= 1
        for related_video in video.related.all():
            logging.warning(depth)
            crawl_video(related_video, depth)




