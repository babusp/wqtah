"""
tests file
"""

# Create your tests here.

from rest_framework.test import APITestCase
from apps.accounts.models.auth import User


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = "http://localhost:8000/v1/login/"

        self.user_data = {"email_or_phoneNo": "kiwi@gmail.com", "password": "admin"}

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestView(TestSetUp):
    def test_user_register(self):
        res = self.client.post(self.register_url, self.user_data, format="json")
        print("res................", res.data)

        self.assertEqual(
            res.data["email_or_phoneNo"], self.user_data["email_or_phoneNo"]
        )
        self.assertEqual(res.status_code, 201)

    def test_user_login_after_verification(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        print("res................", response.data)

        email = response.data["email_or_phoneNo"]
        print("email................", email)

        user = User.objects.filter(email=email)
        print("user................", user)

        user.is_verified = True
        user.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)
