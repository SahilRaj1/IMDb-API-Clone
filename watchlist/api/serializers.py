from rest_framework import serializers
from watchlist.models import Movie

# validation using validators
def genre_length(value):
    if len(value)<4:
        raise serializers.ValidationError("Invalid Genre")

# Classic Serializers
class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    review = serializers.CharField()
    genre = serializers.CharField(validators=[genre_length])

    # for post requests (adding new data)
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    # for put requests (updating data)
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.review = validated_data.get('review', instance.review)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.save()
        return instance

    # field level validation
    def validate_review(self, value):
        if len(value)<4:
            raise serializers.ValidationError("Review too short")
        else:
            return value

    # object level validation
    def validate(self, data):
        if data['title'] == data['review']:
            raise serializers.ValidationError("Invalid review")
        else:
            return data
