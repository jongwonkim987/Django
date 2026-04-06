from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword1234",
        }
        self.user = User.objects.create_user(**self.data)

    def test_jwt_login(self):
        data = {
            "username": self.data["username"],
            "password": self.data["password"],
        }
        response = self.client.post(reverse("jwt-login"), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_jwt_verify(self):
        login_response = self.client.post(
            reverse("jwt-login"),
            {"username": self.data["username"], "password": self.data["password"]},
        )
        access_token = login_response.data["access"]

        response = self.client.post(reverse("jwt-verify"), {"token": access_token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_refresh(self):
        login_response = self.client.post(
            reverse("jwt-login"),
            {"username": self.data["username"], "password": self.data["password"]},
        )
        refresh_token = login_response.data["refresh"]

        response = self.client.post(reverse("jwt-refresh"), {"refresh": refresh_token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
