from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

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
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    release_year = models.IntegerField()
    director = models.CharField(max_length=50)
    description = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title