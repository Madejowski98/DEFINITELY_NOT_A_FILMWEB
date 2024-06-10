from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Review, Article, Genre
from .forms import MovieForm, ReviewForm, ArticleForm, GenreForm


# MOVIE VIEWS
# movie list view
def movie_list(request):
    movies = Movie.objects.filter(approved=True)
    genres = Genre.objects.all()

    # filter by release date
    year = request.GET.get("year")
    if year:
        movies = movies.filter(release_year=year)

    # filter by genre
    genre_id = request.GET.get("genre")
    if genre_id:
        movies = movies.filter(genre_id=genre_id)

    context = {
        "movies": movies,
        "genres": genres,
    }
    return render(request, "movies_app/movie_list.html", context)


# movie detail views
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, approved=True)
    reviews = Review.objects.filter(movie=movie)
    average_rating = movie.average_rating
    return render(
        request,
        "movies_app/movie_detail.html",
        {"movie": movie, "reviews": reviews, "average_rating": average_rating},
    )


# adding movie view
@login_required
def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            return redirect("movie_list")
    else:
        form = MovieForm()
    return render(request, "movies_app/add_movie.html", {"form": form})


# admin approval view
@login_required
def approve_movie(request, movie_id):
    if request.user.is_staff:
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.approved = True
        movie.save()
        messages.success(request, f'The movie "{movie.title}" has been approved.')
        return redirect("pending_movies")
    else:
        messages.error(request, "You do not have permission to approve movies.")
        return redirect("home")


@login_required
def reject_movie(request, movie_id):
    if request.user.is_staff:
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.delete()
        messages.success(
            request, f'The movie "{movie.title}" has been rejected and deleted.'
        )
        return redirect("pending_movies")
    else:
        messages.error(request, "You do not have permission to reject movies.")
        return redirect("home")


@login_required
def pending_movies(request):
    if request.user.is_staff:
        movies = Movie.objects.filter(approved=False)
        return render(request, "movies_app/pending_movies.html", {"movies": movies})
    else:
        messages.error(request, "You do not have permission to view pending movies.")
        return redirect("home")


# list of all genres
def genre_list(request):
    genres = Genre.objects.all()
    return render(request, "movies_app/genre_list.html", {"genres": genres})


# adding a new genre
@login_required
def add_genre(request):
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("genre_list")
    else:
        form = GenreForm()
    return render(request, "movies_app/add_genre.html", {"form": form})


# list of articles view
def article_list(request):
    articles = Article.objects.filter(approved=True).order_by("-created_at")[:5]
    return render(request, "movies_app/article_list.html", {"articles": articles})


# article details
def article_detail(request, article_id):
    if request.user.is_staff:
        article = get_object_or_404(Article, pk=article_id)
    else:
        article = get_object_or_404(Article, pk=article_id, approved=True)

    return render(request, "movies_app/article_detail.html", {"article": article})


# adding a new article
@login_required
def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.added_by = request.user
            article.save()
            return redirect("article_list")
    else:
        form = ArticleForm()
    return render(request, "movies_app/add_article.html", {"form": form})


@login_required
def approve_article(request, article_id):
    if request.user.is_staff:
        article = get_object_or_404(Article, pk=article_id)
        article.approved = True
        article.save()
        messages.success(request, f'The article "{article.title}" has been approved.')
        return redirect("pending_articles")
    else:
        messages.error(request, "You do not have permission to approve articles.")
        return redirect("home")


@login_required
def reject_article(request, article_id):
    if request.user.is_staff:
        article = get_object_or_404(Article, pk=article_id)
        article.delete()
        messages.success(
            request, f'The article "{article.title}" has been rejected and deleted.'
        )
        return redirect("pending_articles")
    else:
        messages.error(request, "You do not have permission to reject articles.")
        return redirect("home")


@login_required
def pending_articles(request):
    if request.user.is_staff:
        articles = Article.objects.filter(approved=False)
        return render(
            request, "movies_app/pending_articles.html", {"articles": articles}
        )
    else:
        messages.error(request, "You do not have permission to view pending articles.")
        return redirect("home")


# adding a new review
@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, "Review added successfully.")
            return redirect("movie_detail", movie_id=movie.id)
    else:
        form = ReviewForm()
    return render(request, "movies_app/add_review.html", {"form": form, "movie": movie})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully.")
            return redirect("movie_detail", movie_id=review.movie.id)
    else:
        form = ReviewForm(instance=review)
    return render(
        request, "movies_app/review_update.html", {"form": form, "review": review}
    )


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if request.method == "POST":
        movie_id = review.movie.id
        review.delete()
        messages.success(request, "Review deleted successfully.")
        return redirect("movie_detail", movie_id=movie_id)
    return render(request, "movies_app/review_delete_confirm.html", {"review": review})


# home view
def home(request):
    latest_movies = Movie.objects.filter(approved=True).order_by("-release_year")[:5]
    recent_reviews = Review.objects.order_by("-created_at")[:5]
    latest_articles = Article.objects.filter(approved=True).order_by("-created_at")[:5]

    context = {
        "latest_movies": latest_movies,
        "recent_reviews": recent_reviews,
        "latest_articles": latest_articles,
    }
    return render(request, "movies_app/home.html", context)


# about view
def about(request):
    return render(request, "movies_app/about.html")


# contact view
def contact(request):
    return render(request, "movies_app/contact.html")
