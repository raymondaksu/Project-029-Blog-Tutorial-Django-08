from rest_framework.test import APITestCase
from django.urls import reverse

# Register with valid entries
# Password might be invalid
# Username already registered
# Register section shouldnt be display on register page if logged in (session)
# Register section shouldnt be display on register page if logged in (token) (403)

class UserRegistrationTestCase(APITestCase):
    url = reverse("account:register")
    url_token = reverse("token_obtain_pair")


    def test_user_registration(self):
        """
            Register with valid entries
        """

        data = {
            "username" : "usertest",
            "email" : "usertest@gmail.com",
            "password" : "Ra741258"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)


    def test_user_invalid_password(self):
        """
            Password might be invalid
        """

        data = {
            "username" : "usertest",
            "email" : "usertest@gmail.com",
            "password" : "1"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)


    def test_unique_name(self):
        """
            Check whether name is unique or not
        """

        self.test_user_registration()
        data = {
            "username" : "usertest",
            "password" : "Ra856987"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)


    def test_user_authenticated_registration(self):
        """
            Register section shouldnt be display on register page if logged in (session)
        """

        self.test_user_registration()
        self.client.login(username="usertest", password='Ra741258')
        response = self.client.get(self.url)

        self.assertEqual(405, response.status_code)

        
    def test_user_authenticated_token_registration(self):
        """
            Register section shouldnt be display on register page if logged in (token) (403)
        """

        self.test_user_registration()
        data = {
            "username" : "usertest",
            "email" : "usertest@gmail.com",
            "password" : "Ra741258"
        }
        response = self.client.post(self.url_token, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response_2 = self.client.get(self.url)
        self.assertEqual(403, response_2.status_code)


