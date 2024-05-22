from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from accounts.forms import UserProfileModelForm
from accounts.models import UserProfile


@login_required
def user_profile_create(request):
    if request.method == "GET":
        is_profile_exist = UserProfile.objects.filter(user=request.user).exists()
        if is_profile_exist:
            return redirect("my_user_profile")
        form = UserProfileModelForm()
        ctx = {
            "form": form,
        }
        return render(request, "accounts/user_profile_create.html", ctx)

    if request.method == "POST":
        form = UserProfileModelForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            messages.success(request, "Your profile has been created successfully!")
            return redirect("my_user_profile")

        ctx = {
            "form": form,
        }
        return render(request, "accounts/user_profile_create.html", ctx)


@login_required
def my_user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    ctx = {
        "user_profile": user_profile,
    }
    return render(request, "accounts/my_user_profile.html", ctx)


class LogoutConfirmView(View):
    def get(self, request):
        return render(request, "registration/logout_confirm.html")


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        ctx = {
            "form": form,
        }
        return render(request, "registration/register.html", ctx)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")

        ctx = {
            "form": form,
        }
        return render(request, "registration/register.html", ctx)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'registration/login2.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'registration/login2.html')