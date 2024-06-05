from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    """
    The Review model represents a user review for a specific movie.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    review = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.movie} - {self.rating}"


class Movie(models.Model):
    """
    The Movie model represents a film with its title, genre, release year,
    director, description, the user who added it, and timestamps for creation and updates.
    """

    title = models.CharField(max_length=255)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    release_year = models.IntegerField()
    director = models.CharField(max_length=50)
    description = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="media/", null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        reviews = self.review_set.all()
        if reviews.exists():
            return reviews.aggregate(models.Avg("rating"))["rating__avg"]
        return 0


class Article(models.Model):
    """
    The Article model represents an article with its title, description,
    the user who added it, and timestamps for creation.
    Model updated with approve/reject methods.
    """

    title = models.CharField(max_length=255)
    description = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to="media/", null=True, blank=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    """ """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
