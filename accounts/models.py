from django.conf import settings
from django.db import models

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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return f"Profile of {self.user}"
