from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class UserProfile(models.Model):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    )

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Profile of {self.user}"