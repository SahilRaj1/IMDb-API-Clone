from rest_framework.response import Response
from rest_framework import status
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from watchlist.models import WatchList, StreamPlatform, Review
from watchlist.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer


# Routes for all reviews
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # overwriting queryset
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


# Routes for a specific review
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# Route for creating review for a specific movie
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    # overwriting create method
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        serializer.save(watchlist=watchlist)


# # Routes for all reviews
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     # endpoint to fetch all reviews
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     # endpoint to add a new review
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# # Routes for a specific review
# class ReviewDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     # endpoint to fetch a specific review
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     # endpoint to fetch all reviews
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     # endpoint to fetch all reviews
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


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


# # Routes for streaming platforms
# class StreamPlatformViewSet(viewsets.ViewSet):
#
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         platform = generics.get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def update(self, request, pk):
#         queryset = StreamPlatform.objects.all()
#         platform = generics.get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         queryset = StreamPlatform.objects.all()
#         platform = generics.get_object_or_404(queryset, pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# Routes for streaming platforms
class StreamPlatformViewSet(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


# # Routes for all streaming platforms
# class StreamPlatformAV(APIView):
#
#     # endpoint to fetch all platforms
#     def get(self, request):
#         platforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platforms, many=True)
#         return Response(serializer.data)
#
#     # endpoint to add a new platform
#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # Routes for a specific platform
# class StreamPlatformDetailAV(APIView):
#
#     # endpoint to fetch a specific platform by id
#     def get(self, request, pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({"error": "Platform not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data)
#
#     # endpoint to update a specific platform by id
#     def put(self, request, pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({"error": "Platform not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = StreamPlatformSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # endpoint to delete a specific platform by id
#     def delete(self, request, pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({"error": "Platform not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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
