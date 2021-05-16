from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
import json

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

class UserLogin(APITestCase):
    url_token = reverse("token_obtain_pair")

    # working this func before run tests
    def setUp(self):
        self.username = "aksu"
        self.password = "Ra852963"
        self.user = User.objects.create_user(username = self.username, password=self.password)

    def test_user_token(self):
        response = self.client.post(self.url_token, {"username": "aksu" , "password": "Ra852963"})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
    
    def test_user_invalid_data(self):
        response = self.client.post(self.url_token, {"username": "invalid" , "password": "Ra852963"})
        self.assertEqual(401, response.status_code)
    
    def test_user_empty_data(self):
        response = self.client.post(self.url_token, {"username": "" , "password": ""})
        self.assertEqual(400, response.status_code)


class UserPasswordChange(APITestCase):
    url = reverse("account:change-password")
    url_token = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "aksu"
        self.password = "Ra852963"
        self.user = User.objects.create_user(username = self.username, password=self.password)

    def login_with_token(self):
        data = {
            "username" : "aksu",
            "password" : "Ra852963"
        }
        response = self.client.post(self.url_token, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)


    # Check try change password without login
    def test_is_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
        

    # Check try change password with valid token
    def test_with_valid_informations(self):
        self.login_with_token()
        data = {
            "old_password" : "Ra852963",
            "new_password" : "Ra987654"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(204, response.status_code)


    # Check try change password with invalid old_password
    def test_with_invalid_informations(self):
        self.login_with_token()
        data = {
            "old_password" : "Ra123456",
            "new_password" : "Ra987654"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(400, response.status_code)


    # Check try change password with empty info
    def test_with_empty_informations(self):
        self.login_with_token()
        data = {
            "old_password" : "",
            "new_password" : ""
        }
        response = self.client.put(self.url, data)
        self.assertEqual(406, response.status_code)


class UserProfileUpdate(APITestCase):
    url = reverse("account:me")
    url_token = reverse("token_obtain_pair")


    def setUp(self):
        self.username = "aksu"
        self.password = "Ra852963"
        self.user = User.objects.create_user(username = self.username, password=self.password)

    def login_with_token(self):
        data = {
            "username" : "aksu",
            "password" : "Ra852963"
        }
        response = self.client.post(self.url_token, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    

    # Check try update profile without login
    def test_is_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)


    # Check try update profile with valid info
    def test_with_valid_informations(self):
        self.login_with_token()
        data = {
            "id" : 1,
            "first_name" : "",
            "last_name" : "",
            "profile" : {
                "id" : 1,
                "note" : "",
                "twitter" : "",
            }
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), data)

