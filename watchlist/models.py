from django.db import models

# Create your models here.

# Watch lists
class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name

# Streaming Platforms
class WatchList(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    genre = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
