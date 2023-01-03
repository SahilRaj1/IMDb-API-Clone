from rest_framework.response import Response
from watchlist.models import Movie
from rest_framework import status
from watchlist.api.serializers import MovieSerializer
# from rest_framework.decorators import api_view
from rest_framework.views import APIView

# Routes for all movies
class MoivesAV(APIView):

    # endpoint to fetch all movies
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    # endpoint to add a new movie
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Routes for a specific movie
class MovieDetailAV(APIView):

    # endpoint to fetch a specific movie by id
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    # endpoint to update a specific movie by id
    def put(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # endpoint to delete a specific movie by id
    def delete(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# # Routes for all movies
# @api_view(['GET', 'POST'])
# def movies(request):
#     # endpoint to fetch all movies
#     if request.method == 'GET':
#         movie_list = Movie.objects.all()
#         serializer = MovieSerializer(movie_list, many=True)
#         return Response(serializer.data)
#     # endpoint to add a new movie
#     elif request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
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
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
#
#     # endpoint to fetch a specific movie by id
#     if request.method == 'GET':
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#     # endpoint to update a specific movie by id
#     elif request.method == 'PUT':
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # endpoint to delete a specific movie by id
#     elif request.method == 'DELETE':
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
