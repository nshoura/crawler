from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100, blank=True, null = True) # Name of the tag

class Site(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

class Video(models.Model):
    video_url = models.URLField(blank=True, null = True)
    video_api_url = models.URLField(blank=True, null = True)
    site = models.ForeignKey('site')
    description = models.TextField(blank=True, null = True) # Comprehensive description of this video.
    embed_html = models.TextField(blank=True, null = True) # HTML embedding code.
    video_id = models.CharField(max_length=150, unique=True) # The video object ID
    owner_name = models.CharField(max_length=200, blank=True, null = True) #name of the owner of this video.
    owner_id = models.CharField(max_length=200, blank=True, null = True)
    owner_url=models.URLField(blank=True, null = True) #URL to the owner of this video.
    tags = models.ManyToManyField(Tag, blank = True, null=True) # List of tags attached to this video.
    thumbnail_url = models.URLField(blank=True, null = True) # URL of this video's raw thumbnail (full size respecting ratio).
    title = models.CharField(max_length=300, blank=True, null = True) # Title of this video.
    related = models.ManyToManyField('self', blank = True, null=True) # List of videos related to this video.
    views_total = models.IntegerField(blank=True, null = True) #Total amount of views on this video since its publication.
    def __unicode__(self):
        return self.video_id
