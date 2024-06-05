from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "gender"]
        help_texts = {
            "username": None,
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, gender=self.cleaned_data["gender"])
        return user


class UserProfileEditForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = ["gender"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["email"].initial = user.email
