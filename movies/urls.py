from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('new/', views.movie_create, name='movie_create'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
    path('<int:pk>/edit/', views.movie_edit, name='movie_edit'),
    path('<int:pk>/delete/', views.movie_delete, name='movie_delete'),
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
]