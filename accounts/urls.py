from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import (
    RegisterView,
    LogoutConfirmView,
    my_user_profile,
    delete_account,
    delete_account_confirm,
    login_view,
    profile_update,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("logout_confirm/", LogoutConfirmView.as_view(), name="logout_confirm"),
    path("register/", RegisterView.as_view(), name="register"),
    path("my_profile/", my_user_profile, name="my_user_profile"),
    path("profile_update/", profile_update, name="profile_update"),
    path(
        "delete_account_confirm/", delete_account_confirm, name="delete_account_confirm"
    ),
    path("delete_account/", delete_account, name="delete_account"),
]
