from django.db import models

# Create your models here.
class YoutubeData(models.Model):
    title = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    published_on = models.DateTimeField()
    thumnail_url = models.CharField(max_length=2048, blank=True, null=True)
