from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.email = "test@example.com"
        self.nickname = "testuser"
        self.password = "testpassword123"

    def test_user_manager_create_user(self):
        user = User.objects.create_user(
            email=self.email,
            nickname=self.nickname,
            password=self.password,
        )
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.nickname, self.nickname)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_user_manager_create_superuser(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            nickname="adminuser",
            password=self.password,
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password(self.password))
