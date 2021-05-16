from comment.models import Comment
from post.models import Post
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
import json

class CommentCreateTest(APITestCase):
    login_url = reverse("token_obtain_pair")

    def setUp(self):
        self.url = reverse("comment:create")
        self.url_list = reverse("comment:list")
        self.username = "aksu"
        self.password = "aksu789456"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.post = Post.objects.create(user= self.user, title="comment title", content="comment content")
        self.parent_comment = Comment.objects.create(content="parent content", user=self.user, post=self.post)
        self.jwt_authentication()

    def jwt_authentication(self):
        response = self.client.post(self.login_url, data={"username" : "aksu", "password" : "aksu789456"})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
    

    # create comment
    def test_create_comment_with_valid_entries(self):
        data = {
            "content" : "test comment 1",
            "modified_at" : "2020-05-12 15:30",
            "user" : self.user.id,
            "post" : self.post.id,
            "parent" : ""
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    # create child comment
    def test_create_child_comment_with_valid_entries(self):
        data = {
            "content" : "test comment 1",
            "modified_at" : "2020-05-12 15:30",
            "user" : self.user.id,
            "post" : self.post.id,
            "parent" : self.parent_comment.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    # create child comment
    def test_comment_list(self):
        self.test_create_comment_with_valid_entries()
        response = self.client.get(self.url_list, {"q" : self.post.id})
        self.assertTrue(response.data["count"] == Comment.objects.filter(post = self.post.id).count())


class CommentUpdateDeleteTest(APITestCase):
    login_url = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "aksu"
        self.password = "aksu789456"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user("ramazan", password=self.password)
        self.post = Post.objects.create(user= self.user, title="comment title", content="comment content")
        self.comment = Comment.objects.create(content="parent content", user=self.user, post=self.post)
        self.url = reverse("comment:update", kwargs={"pk": self.comment.pk})
        self.test_jwt_authentication()

    def test_jwt_authentication(self, username="aksu", password="aksu789456"):
        response = self.client.post(self.login_url, data={"username" : username, "password" : password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # delete comment
    def test_delete_comment(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
        self.assertFalse(Comment.objects.filter(pk = self.comment.pk).exists())

    # checking try delete comment by different user
    def test_delete_comment_by_other_user(self):
        self.test_jwt_authentication(username="ramazan")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)
        self.assertTrue(Comment.objects.get(pk = self.comment.pk))

    # update comment
    def test_update_comment(self):
        response = self.client.put(self.url, data={"content" : "new one"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(Comment.objects.get(pk = self.comment.pk).content, "new one")

    # checking try update comment by different user
    def test_update_by_different_user(self):
        self.test_jwt_authentication("ramazan")
        response = self.client.put(self.url, data={"content" : "new one"})
        self.assertEqual(403, response.status_code)
        self.assertNotEqual(Comment.objects.get(pk = self.comment.pk).content, "new one")

    # try reach update page without login
    def test_authorization(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)