from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from owner.models import Owner


class TestLeagueLeadersView(APITestCase):
    url = "/login/"

    def setUp(self):
        self.user = Owner.objects.create_owner(
            name="User1",
            username="user.one",
            password="password",
        )

    def test_login(self):
        request_data = {
            "username": self.user.username,
            "password": "password",
        }
        response = self.client.get(self.url, data=request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data["token"]
        expected_token = Token.objects.get(key=token).key
        self.assertEqual(expected_token, token)
