from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views

from config import settings
from movies_app import views


urlpatterns = [
    path('movie_list/', views.movie_list, name='movie_list'),
    path('movie_detail/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('add_movie', views.add_movie, name='add_movie'),
    path('add_review<int:movie_id>/', views.add_review, name='add_review'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('add_article', views.add_article, name='add_article'),
    path('genres/', views.genre_list, name='genre_list'),
    path('add_genre', views.add_genre, name='add_genre'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('approve_movie/<int:movie_id>/', views.approve_movie, name='approve_movie'),
    path('reject_movie/<int:movie_id>/', views.reject_movie, name='reject_movie'),
    path('pending_movies/', views.pending_movies, name='pending_movies'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)