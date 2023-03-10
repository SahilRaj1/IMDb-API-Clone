from rest_framework.response import Response
from rest_framework import status
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from watchlist.models import WatchList, StreamPlatform, Review
from watchlist.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist.api.permissions import AdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist.api.throttling import ReviewListThrottle, ReviewCreateThrottle
from watchlist.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination


# Routes for all reviews
class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # throttle_classes = [AnonRateThrottle, ReviewListThrottle]

    # overwriting queryset
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(created_by__username=username)

    def get_queryset(self):
        queryset = Review.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(created_by__username=username)
        return queryset


# Routes for all reviews
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes = [AnonRateThrottle, ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__username', 'valid']

    # overwriting queryset
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


# Routes for a specific review
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


# Route for creating review for a specific movie
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    # overwriting create method
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        created_by = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, created_by=created_by)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed for this project")

        watchlist.avg_rating = (watchlist.avg_rating * watchlist.number_rating + serializer.validated_data['rating'])/(watchlist.number_rating+1)
        watchlist.number_rating += 1
        watchlist.save()

        serializer.save(watchlist=watchlist, created_by=created_by)


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
class WatchListAV(generics.ListCreateAPIView):

    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'platform__name']
    ordering_fields = ['avg_rating']
    pagination_class = WatchListLOPagination

    # # endpoint to fetch all movies
    # def get(self, request):
    #     movies = WatchList.objects.all()
    #     serializer = WatchListSerializer(movies, many=True)
    #     return Response(serializer.data)
    #
    # # endpoint to add a new movie
    # def post(self, request):
    #     serializer = WatchListSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Routes for a specific movie
class WatchListDetailAV(APIView):

    permission_classes = [AdminOrReadOnly]

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
    permission_classes = [AdminOrReadOnly]


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
