from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CharField, Model, IntegerField, DecimalField, DateTimeField, ForeignKey, TextField
from django.utils import timezone
from django.conf import settings
User = settings.AUTH_USER_MODEL

"""
    I have created a Review model imported from django.db.models that will take user_id as a IntegerField,
    movie_id that will take a IntergerField, rating taking a IntegerField with minimum value of 1 and maximum of 10,
    review taking a CharField with a maximum length of 255 characters,
    created_at which will be a DateTimeField,
    added_by a ForeignKey to User model.
"""
class Review(models.Model):
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    review = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review

# Genre constants definitions
ACTION = "ACTION"
ADVENTURE = "ADVENTURE"
ANIMATION = "ANIMATION"
COMEDY = "COMEDY"
CRIME = "CRIME"
DRAMA = "DRAMA"
DOCUMENTARY = "DOCUMENTARY"
SCI_FI = "SCI-FI"
FAMILY = "FAMILY"
HISTORY = "HISTORY"
FANTASY = "FANTASY"
HORROR = "HORROR"
MUSICAL = "MUSICAL"
MYSTERY = "MYSTERY"
ROMANCE = "ROMANCE"
THRILLER = "THRILLER"
WAR = "WAR"
WESTERN = "WESTERN"

# Genre choices list
GENRE_CHOICES = (
    (ACTION, "Action"),
    (ADVENTURE, "Adventure"),
    (ANIMATION, "Animation"),
    (COMEDY, "Comedy"),
    (CRIME, "Crime"),
    (DRAMA, "Drama"),
    (DOCUMENTARY, "Documentary"),
    (SCI_FI, "Sci-Fi"),
    (FAMILY, "Family"),
    (HISTORY, "History"),
    (FANTASY, "Fantasy"),
    (HORROR, "Horror"),
    (MUSICAL, "Musical"),
    (MYSTERY, "Mystery"),
    (ROMANCE, "Romance"),
    (THRILLER, "Thriller"),
    (WAR, "War"),
    (WESTERN, "Western"),
)


class Movie(models.Model):
    """ The Movie model represents a film with its title, genre, release year,
    director, description, the user who added it, and timestamps for creation and updates.
    """
    title = models.CharField(max_length=255)  # The title of the movie"""
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    release_year = models.IntegerField()
    director = models.CharField(max_length=50)
    description = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Article(models.Model):
    title = CharField(max_length=255)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = TextField(blank=False)

    def __str__(self):
        return self.title