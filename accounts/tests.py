from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile
from accounts.forms import CustomUserCreationForm, UserProfileEditForm


class AccountTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.user_profile = UserProfile.objects.create(user=self.user, gender="MALE")
        self.client.login(username="testuser", password="12345")

    def test_login_valid(self):
        self.client.logout()
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "12345"}
        )
        self.assertRedirects(response, reverse("my_user_profile"))

    def test_login_invalid(self):
        self.client.logout()
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertContains(response, "Invalid credentials")

    def test_register(self):
        self.client.logout()
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "password123",
                "password2": "password123",
                "gender": "FEMALE",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(
            UserProfile.objects.filter(
                user__username="newuser", gender="FEMALE"
            ).exists()
        )

    def test_register_password_mismatch(self):
        self.client.logout()
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "password123",
                "password2": "password456",
                "gender": "FEMALE",
            },
        )
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertEqual(form.errors["password2"], ["Passwords don't match"])
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_profile_update_valid(self):
        response = self.client.post(
            reverse("profile_update"),
            {"email": "newemail@example.com", "gender": "OTHER"},
        )
        self.assertRedirects(response, reverse("my_user_profile"))
        self.user.refresh_from_db()
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")
        self.assertEqual(self.user_profile.gender, "OTHER")

    def test_profile_update_invalid(self):
        response = self.client.post(
            reverse("profile_update"), {"email": "invalid-email", "gender": "OTHER"}
        )
        self.assertContains(response, "Enter a valid email address")
        self.user.refresh_from_db()
        self.user_profile.refresh_from_db()
        self.assertNotEqual(self.user.email, "invalid-email")

    def test_delete_account_confirm(self):
        response = self.client.get(reverse("delete_account_confirm"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/delete_account_confirm.html")

    def test_delete_account(self):
        response = self.client.post(reverse("delete_account"))
        self.assertRedirects(response, reverse("login"))
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_my_user_profile(self):
        response = self.client.get(reverse("my_user_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/my_user_profile.html")
        self.assertContains(response, "My Profile")
