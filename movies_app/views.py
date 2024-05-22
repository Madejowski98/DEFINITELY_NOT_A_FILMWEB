from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Review, Article, Genre
from .forms import MovieForm, ReviewForm, ArticleForm, GenreForm


