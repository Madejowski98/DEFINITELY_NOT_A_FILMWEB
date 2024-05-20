from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CharField, Model, IntegerField, DecimalField, DateTimeField, ForeignKey
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
class Review(Model):
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    review = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)