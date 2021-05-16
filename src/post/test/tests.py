from post.models import Post
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
import json


class PostCreateListTest(APITestCase):
    url_create = reverse("post:create")
    url_list = reverse("post:list")
    url_token = reverse("token_obtain_pair")


    def setUp(self):
        self.username = "aksu"
        self.password = "Ra852963"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_token, data={"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # add post
    def test_add_new_post(self):
        data = {
            "content" : "text123",
            "title" : "baslik"
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(201, response.status_code)

    # add post without authorization
    def test_add_new_post_without_authorization(self):
        self.client.credentials()
        data = {
            "content" : "text123",
            "title" : "baslik"
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(401, response.status_code)

    # tests posts list
    def test_posts(self):
        self.test_add_new_post()
        response = self.client.get(self.url_list)
        self.assertTrue(len(json.loads(response.content)["results"]) == Post.objects.all().count())


class PostUpdateDeleteTest(APITestCase):
    login_url = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "aksu"
        self.password = "Ra852963"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="aksu1", password="Ra789456")
        self.post = Post.objects.create(user= self.user, title="Baslik", content="icerik")
        self.url = reverse("post:update", kwargs={"slug":self.post.slug})
        self.test_jwt_authentication()
    
    def test_jwt_authentication(self, username = "aksu", password = "Ra852963"):
        response = self.client.post(self.login_url, data={"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
    
    #delete post test
    def test_post_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)

    #delete post test by different user
    def test_post_delete_by_different_user(self):
        self.test_jwt_authentication(username="aksu1", password="Ra789456")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    #update post test
    def test_post_update(self):
        data = {
            "content" : "post content updated",
            "title" : "post title updated"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(Post.objects.get(id = self.post.id).content, data["content"])

    #update post test by different user
    def test_post_update_by_different_user(self):
        self.test_jwt_authentication(username="aksu1", password="Ra789456")
        data = {
            "content" : "post content updated",
            "title" : "post title updated"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(403, response.status_code)
        self.assertFalse(Post.objects.get(id = self.post.id).content == data["content"])

    # test try reach page without unauthorization
    def test_unauthorization(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
