from rest_framework import serializers
from watchlist.models import WatchList, StreamPlatform


# WatchList Serializer
class WatchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchList
        fields = "__all__"


# StreamPlatform Serializer
class StreamPlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = StreamPlatform
        fields = "__all__"
