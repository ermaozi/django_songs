from django.db import models


class songs(models.Model):
    songs_id = models.IntegerField()
    title = models.CharField(max_length=100)
    singer = models.CharField(max_length=100)
    songUrl = models.CharField(max_length=300)
    imageUrl = models.CharField(max_length=300)