from django.db import models
from django.contrib.auth.models import User
from post.models import Post
from django.utils import timezone

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.post.title + " " + self.user.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Comment, self).save(*args, **kwargs) 
    
    def children(self):
        return Comment.objects.filter(parent=self)
    
    @property
    def any_children(self):
        return Comment.objects.filter(parent=self).exists()
    
