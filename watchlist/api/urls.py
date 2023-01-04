from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist.api import views

router = DefaultRouter()
router.register(r'platforms', views.StreamPlatformViewSet, basename='platform')

urlpatterns = [
    path('watchlist/', views.WatchListAV.as_view(), name='movies'),
    path('watchlist/<int:pk>/', views.WatchListDetailAV.as_view(), name='movie'),

    path('', include(router.urls)),
    # path('platforms/', views.StreamPlatformAV.as_view(), name='platforms'),
    # path('platforms/<int:pk>/', views.StreamPlatformDetailAV.as_view(), name='platform'),

    path('watchlist/<int:pk>/reviews/', views.ReviewList.as_view(), name='reviews'),
    path('watchlist/<int:pk>/review-create/', views.ReviewCreate.as_view(), name='reviews'),
    path('watchlist/reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review'),
]
