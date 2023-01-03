from rest_framework.response import Response
from watchlist.models import WatchList, StreamPlatform
from rest_framework import status
from watchlist.api.serializers import WatchListSerializer, StreamPlatformSerializer
# from rest_framework.decorators import api_view
from rest_framework.views import APIView


# Routes for all movies
class WatchListAV(APIView):

    # endpoint to fetch all movies
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    # endpoint to add a new movie
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Routes for a specific movie
class WatchListDetailAV(APIView):

    # endpoint to fetch a specific movie by id
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"error": "WatchList not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    # endpoint to update a specific movie by id
    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"error": "WatchList not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # endpoint to delete a specific movie by id
    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"error": "WatchList not found"}, status=status.HTTP_404_NOT_FOUND)

        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Routes for all streaming platforms
class StreamPlatformAV(APIView):

    # endpoint to fetch all platforms
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data)

    # endpoint to add a new platform
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # Routes for all movies
# @api_view(['GET', 'POST'])
# def movies(request):
#     # endpoint to fetch all movies
#     if request.method == 'GET':
#         movie_list = WatchList.objects.all()
#         serializer = WatchListSerializer(movie_list, many=True)
#         return Response(serializer.data)
#     # endpoint to add a new movie
#     elif request.method == 'POST':
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# # Routes for a specific movie
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
#
#     # finding the movie by id
#     try:
#         movie = WatchList.objects.get(pk=pk)
#     except WatchList.DoesNotExist:
#         return Response({"error": "WatchList not found"}, status=status.HTTP_404_NOT_FOUND)
#
#     # endpoint to fetch a specific movie by id
#     if request.method == 'GET':
#         serializer = WatchListSerializer(movie)
#         return Response(serializer.data)
#     # endpoint to update a specific movie by id
#     elif request.method == 'PUT':
#         serializer = WatchListSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # endpoint to delete a specific movie by id
#     elif request.method == 'DELETE':
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
