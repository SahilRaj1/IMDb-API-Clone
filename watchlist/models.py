from django.db import models

# Create your models here.

class WatchList(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    genre = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name
