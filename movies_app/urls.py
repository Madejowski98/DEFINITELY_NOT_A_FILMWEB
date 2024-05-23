from django.urls import path
from django.contrib.auth import views as auth_views

from movies_app import views


urlpatterns = [
    path("movie/<int:pk>", views.movie_detail, name="movie_detail"),
    path("genre_list", views.genre_list, name="genre_list"),
    path("movie_list", views.movie_list, name="movie_list"),
    path("movie_detail/<int:pk>", views.movie_detail, name="movie_detail"),
    path("add_genre", views.add_genre, name="add_genre"),
    path("add_movie", views.add_movie, name="add_movie"),
]