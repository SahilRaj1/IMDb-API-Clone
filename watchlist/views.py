# from django.shortcuts import render, HttpResponse
# from django.http import JsonResponse
# from watchlist.models import Movie
#
# # Create your views here.
# def index(request):
#     return HttpResponse('My name is Sahil')
#
# def movies(request):
#     movie_list = Movie.objects.all()
#     data = {
#         'movies': list(movie_list.values())
#     }
#     return JsonResponse(data)
#
# def movie_detail(request, pk):
#     movie = Movie.objects.get(pk=pk)
#     data = {
#        'title': movie.title,
#         'review': movie.review,
#         'genre': movie.genre
#     }
#     return JsonResponse(data)
