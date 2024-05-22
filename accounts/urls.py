from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import RegisterView, LogoutConfirmView, my_user_profile, user_profile_create, login_view

urlpatterns = [
    path("user_profile_create", user_profile_create, name="user_profile_create"),
    path("my_profile", my_user_profile, name="my_user_profile"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("login2/", login_view, name="login2"),

    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="registration/logged_out.html"),
        name="logout",
    ),
    path("logout_confirm/", LogoutConfirmView.as_view(), name="logout_confirm"),
    path("register/", RegisterView.as_view(), name="register"),
]