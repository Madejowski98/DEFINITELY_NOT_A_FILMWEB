from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Review, Article, Genre
from .forms import MovieForm, ReviewForm, ArticleForm, GenreForm


## MOVIE VIEWS
## movie list view
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, "movies_app/movie_list.html", {"movies": movies})


## movie detail views
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = movie.reviews.all()
    return render(request, "movies_app/movie_detail.html", {"movie": movie, "reviews": reviews})


## adding movie view
@login_required
def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            return redirect("movie_detail", movie_id=movie.id)
    else:
        form = MovieForm()
    return render(request, "movies_app/add_movie.html", {"form": form})


## list of all genres
def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'movies_app/genre_list.html', {'genres': genres})


## adding a new genre
@login_required
def add_genre(request):
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = GenreForm()
    return render(request, 'movies_app/add_genre.html', {'form': form})