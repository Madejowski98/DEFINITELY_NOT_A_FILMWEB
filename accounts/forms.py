from django import forms
from accounts.models import UserProfile


class UserProfileModelForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["gender"]