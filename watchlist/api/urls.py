from django.urls import path
from watchlist.api import views

urlpatterns = [
    path('watchlist/', views.WatchListAV.as_view(), name='movies'),
    path('watchlist/<int:pk>/', views.WatchListDetailAV.as_view(), name='movie'),
    path('streams/', views.StreamPlatformAV.as_view(), name='movies'),
]
