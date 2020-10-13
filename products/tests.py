from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        user_a = User(username="siva", email="test@gmail.com")
        password = "siva143"
        # User.objects.create()
        # User.objects.create_user()
        user_a.is_staff = True
        user_a.is_superuser = False
        user_a.set_password(password)
        user_a.save()

        User.objects.create_user("chaitu", "testb@gmail.com", password)  # user_b

    def test_user_qs_count(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)
        self.assertNotEqual(user_count, 0)

    def test_invalid_request(self):
        self.client.login(username="chaitu", password="siva143")
        response = self.client.post('/products/create/', {"title": "test invalid request"})
        self.assertNotEqual(response.status_code, 201)

    def test_valid_request(self):
        self.client.login(username="siva", password="siva143")
        response = self.client.post('/products/create/', {"title": "test valid request"})
        self.assertEqual(response.status_code, 201)




