from rest_framework import serializers
from watchlist.models import WatchList, StreamPlatform, Review


# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist', )
        # fields = "__all__"


# WatchList Serializer
class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"


# StreamPlatform Serializer
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"
