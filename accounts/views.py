from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_protect
from accounts.forms import CustomUserCreationForm, UserProfileEditForm
from accounts.models import UserProfile


@csrf_protect
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(my_user_profile)
        else:
            return render(
                request, "registration/login.html", {"error": "Invalid credentials"}
            )
    else:
        return render(request, "registration/login.html", {"next": my_user_profile})


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "registration/register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(
                user=user, defaults={"gender": form.cleaned_data["gender"]}
            )
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")
        return render(request, "registration/register.html", {"form": form})


class LogoutConfirmView(View):
    def get(self, request):
        return render(request, "registration/logout_confirm.html")


@login_required
def my_user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    return render(
        request, "accounts/my_user_profile.html", {"user_profile": user_profile}
    )


@login_required
def delete_account_confirm(request):
    return render(request, "accounts/delete_account_confirm.html")


@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect("login")
    return redirect("my_user_profile")


@login_required
def profile_update(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        form = UserProfileEditForm(
            request.POST, instance=user_profile, user=request.user
        )
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user.email = form.cleaned_data["email"]
            user_profile.user.save()
            user_profile.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("my_user_profile")
    else:
        form = UserProfileEditForm(instance=user_profile, user=request.user)
    return render(request, "accounts/profile_update.html", {"form": form})
