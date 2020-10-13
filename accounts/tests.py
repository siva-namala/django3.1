from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        user = User(username="siva", email="test@gmail.com")
        password = "siva143"
        # User.objects.create()
        # User.objects.create_user()
        user.is_staff = True
        user.is_superuser = True
        user.save()
        user.set_password(password)    # saved after added password
        user.save()

        self.password = password

    def test_user_qs_count(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

    def test_user_exists(self):
        user = User.objects.filter(username__iexact="siva")
        user_exists = user.exists() and user.count() == 1
        self.assertTrue(user_exists)

    def test_user_password(self):
        user = User.objects.get(username="siva")
        self.assertTrue(user.check_password(self.password))

    def test_login_url(self):
        login_url = '/login/'
        data = {"username": "siva", "password": self.password}
        response = self.client.post(login_url, data, follow=True)
        status_code = response.status_code
        redirect_url = response.request.get('PATH_INFO')

        self.assertEqual(settings.LOGIN_URL, login_url)
        self.assertEqual(status_code, 200)
        self.assertEqual(settings.LOGIN_REDIRECT_URL, redirect_url)

