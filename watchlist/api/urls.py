from django.urls import path
from watchlist.api import views

urlpatterns = [
    path('movies/', views.MoivesAV.as_view(), name='movies'),
    path('movies/<int:pk>/', views.MovieDetailAV.as_view(), name='movie'),
]
