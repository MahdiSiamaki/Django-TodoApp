from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("accounts:login")
        self.logout_url = reverse("accounts:logout")
        self.signup_url = reverse("accounts:signup")
        self.token_login_url = reverse("api-v1:login")
        self.token_logout_url = reverse("api-v1:logout")
        self.change_password_url = reverse("api-v1:change-password")
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpassword"}
        )
        self.assertRedirects(response, reverse("todo:todo_list"))

    def test_logout_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)

    def test_signup_url(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_invalid_login(self):
        response = self.client.post(
            self.login_url, {"username": "invaliduser", "password": "invalidpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertContains(response, "Invalid username or password.")

    def test_invalid_signup(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "newuser",
                "password1": "newpassword",
                "password2": "differentpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")
        self.assertContains(response, "The two password fields didn’t match.")

    def test_token_login(self):
        response = self.client.post(
            self.token_login_url, {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_token_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(self.token_logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            self.change_password_url,
            {"old_password": "testpassword", "new_password": "newtestpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password updated successfully.")

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newtestpassword"))

    def test_is_verified_field(self):
        self.assertFalse(self.user.is_verified)
        superuser = User.objects.create_superuser(
            username="superuser", password="superpassword"
        )
        self.assertTrue(superuser.is_verified)

    def test_login_view_with_unverified_user(self):
        unverified_user = User.objects.create_user(
            username="unverifieduser", password="unverifiedpassword"
        )
        response = self.client.post(
            self.token_login_url,
            {"username": "unverifieduser", "password": "unverifiedpassword"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "User account is disabled.")
