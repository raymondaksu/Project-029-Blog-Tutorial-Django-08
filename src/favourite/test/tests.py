from favourite.models import Favourite
from post.models import Post
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
import json


class FavouriteCreateList(APITestCase):
    url = reverse("favourite:list-create")
    url_token = reverse("token_obtain_pair")


    def setUp(self):
        self.username = "aksu"
        self.password = "Ra852963"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.post = Post.objects.create(user= self.user, title="Baslik", content="icerik")
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_token, data={"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
    
    # Add favourite
    def test_add_favourite(self):
        data = {
            "content" : "good content",
            "user" : self.user.id,
            "post" : self.post.id
        }

        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)
    
    def test_user_favourites(self):
        self.test_add_favourite()
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)["results"]) == Favourite.objects.filter(user=self.user).count())

    
class FavouriteUpdateDelete(APITestCase):
    login_url = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "aksu"
        self.password = "Ra852963"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="aksu1", password="Ra789456")
        self.post = Post.objects.create(user= self.user, title="Baslik", content="icerik")
        self.favourite = Favourite.objects.create(content="examples", post=self.post, user=self.user)
        self.url = reverse("favourite:update-delete", kwargs={"pk":self.favourite.pk})
        self.test_jwt_authentication()
    
    def test_jwt_authentication(self, username = "aksu", password = "Ra852963"):
        response = self.client.post(self.login_url, data={"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    
    # delete fav
    def test_fav_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)


    # checking try delete by different user
    def test_fav_delete_different_user(self):
        self.test_jwt_authentication(username="aksu1", password="Ra789456")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)
    

    # update favourite
    def test_update_favourite(self):
        data = {
            "content" : "content 123",
            "post" : self.post.id,
            "user" : self.user.id
        }
        response = self.client.put(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(True, Favourite.objects.get(id=self.favourite.id) == data["content"])
    

    # checking try update by different user
    def test_fav_update_different_user(self):
        self.test_jwt_authentication(username="aksu1", password="Ra789456")
        data = {
            "content" : "content 456",
            "user" : self.user2.id
        }

        response = self.client.put(self.url, data)
        self.assertEqual(403, response.status_code)


    # page cannot display without login
    def test_fav_update_without_login(self):
        # user log out with following line
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)