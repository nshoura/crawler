from django.shortcuts import render, redirect
from django.http import Http404
from crawler.models import *
from searcher import views


import json
import urllib2
import logging

depth=0

def crawl(request):
    video_url_to_crawl = request.GET.get('video_url_to_crawl', '')
    global depth
    depth = request.GET.get('depth', '')
    if not (video_url_to_crawl=="" and depth==""):
        if not depth.isdigit():
            return render(request, 'searcher/error.html', {'error_message':'Please enter a number in the crawling depth field between 0 and 50!'})
        depth=int(depth)
        if depth not in xrange(0, 15):
            return render(request, 'searcher/error.html', {'error_message':'The server is not powerful enough to handle such a depth! Please enter a number in the crawling depth field between 0 and 15'})
        video_url=video_url_to_crawl.replace('%3A',':').replace('%2F','/')
        if 'dailymotion.com' in video_url:
            parse_video(video_url)
            return redirect('/video/'+video_url.split('_')[0].split('/')[-1])
        elif 'youtube.com' in video_url:
            parse_video(video_url)
            return redirect('/video/'+video_url.split('=')[1].split('&')[0])
        else:
            return render(request, 'searcher/error.html', {'error_message':'The URL you provided is not a youtube or dailymotion video, please try again!'})
    return render(request, 'searcher/search.html')

def parse_video(video_url):
    urls_to_parse=[]
    global depth
    if 'dailymotion.com' in video_url:
        try:
            video=Video.objects.get(video_id = video_url.split('_')[0].split('/')[-1])
        except Video.DoesNotExist:
            try:
                video=Video(video_id = video_url.split('_')[0].split('/')[-1], site=Site.objects.get(name='dailymotion.com'))
            except Site.DoesNotExist:
                site=Site(name = 'dailymotion.com')
                site.save()
                video=Video(video_id = video_url.split('_')[0].split('/')[-1], site=Site.objects.get(name='dailymotion.com'))
        video.video_api_url = "https://api.dailymotion.com/video/" + video.video_id
        video.video_url = "http://www.dailymotion.com/video/" + video.video_id

        results =json.loads(urllib2.urlopen(video.video_api_url +"?fields=channel,description,embed_html,embed_url,id,owner,owner.screenname,owner.url,tags,thumbnail_url,title,views_total").read())

        video.description = results['description']
        video.embed_html = results['embed_html']
        video.owner_id=results['owner']
        video.owner_name=results['owner.screenname']
        video.owner_url=results['owner.url']
        video.thumbnail_url = results['thumbnail_url']
        video.title = results['title']
        video.views_total = results['views_total']

        related_videos_data = json.loads(urllib2.urlopen(video.video_api_url+"/related").read())['list']

    if 'youtube.com' in video_url:
        try:
            video=Video.objects.get(video_id = video_url.split('=')[1].split('&')[0])
        except Video.DoesNotExist:
            try:
                video=Video(video_id = video_url.split('=')[1].split('&')[0], site=Site.objects.get(name='youtube.com'))
            except Site.DoesNotExist:
                site=Site(name = 'youtube.com')
                site.save()
                video=Video(video_id = video_url.split('=')[1].split('&')[0], site=Site.objects.get(name='youtube.com'))
        video.video_api_url='https://www.googleapis.com/youtube/v3/videos?key=AIzaSyBp-A5_icKU-m0KuFLf0wOvQwbayFC-JEM&id='+video.video_id
        video.video_url="http://www.youtube.com/watch?v="+video.video_id

        results =json.loads(urllib2.urlopen(video.video_api_url+'&part=snippet,statistics,player&fields=items(id,snippet/title,snippet/description,snippet/thumbnails/default/url,snippet/channelTitle,snippet/channelId,snippet/tags,statistics/viewCount,player/embedHtml)').read())
    
        video.description = results['items'][0]['snippet']['description']
        video.embed_html = (results['items'][0]['player']['embedHtml'])[0:-2]+"></iframe>"
        video.owner_id=results['items'][0]['snippet']['channelId']
        video.owner_name=results['items'][0]['snippet']['channelTitle']
        video.owner_url='http://www.youtube.com/channel/'+results['items'][0]['snippet']['channelId']
        video.thumbnail_url = results['items'][0]['snippet']['thumbnails']['default']['url']
        video.title = results['items'][0]['snippet']['title']
        video.views_total = results['items'][0]['statistics']['viewCount']

        related_videos_data = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&key=AIzaSyBp-A5_icKU-m0KuFLf0wOvQwbayFC-JEM&relatedToVideoId="+video.video_id).read())['items']

    video.save()

    if depth >= 0:
        if video.site.name=='youtube.com':
            for related_video_data in related_videos_data:
                try:
                    related_video=Video.objects.get(video_id = related_video_data['id']['videoId'])
                    video.related.add(related_video)
                except Video.DoesNotExist:
                    related_video_url="http://www.youtube.com/watch?v="+related_video_data['id']['videoId']
                    related_video=Video(video_id = related_video_url.split('=')[1].split('&')[0], site=Site.objects.get(name='youtube.com'))
                    related_video.save()
                    video.related.add(related_video)
                    urls_to_parse.append(related_video_url)
        if video.site.name=='dailymotion.com':
            for related_video_data in related_videos_data:
                try:
                    related_video=Video.objects.get(video_id = related_video_data['id'])
                    video.related.add(related_video)
                except Video.DoesNotExist:
                    related_video_url="http://www.dailymotion.com/video/"+related_video_data['id']
                    related_video=Video(video_id = related_video_url.split('_')[0].split('/')[-1], site=Site.objects.get(name='dailymotion.com'))
                    related_video.save()
                    video.related.add(related_video)
                    urls_to_parse.append(related_video_url)
        depth=depth-1
        while urls_to_parse:
            parse_video(urls_to_parse.pop())
    else:
        return

