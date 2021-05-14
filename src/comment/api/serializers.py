from rest_framework.serializers import ModelSerializer, SerializerMethodField
from comment.models import Comment
from django.contrib.auth.models import User
from post.models import Post

from rest_framework import serializers

class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created_at']
    
    def validate(self, attrs):
        if(attrs["parent"]):
            if attrs["parent"].post != attrs["post"]:
                raise serializers.ValidationError("something went wrong")
        return attrs

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        
class PostCommentSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'slug', 'user', 'title', 'content')

class CommentListSerializer(ModelSerializer):
    replies = SerializerMethodField()
    user = UserSerializer()
    post = PostCommentSerializer()
    class Meta:
        model = Comment
        fields = "__all__"
        # retieve all of data first depth ForeignKey
        # depth = 1
    
    def get_replies(self, obj):
        if obj.any_children:
            return CommentListSerializer(obj.children(), many=True).data

class CommentDeleteUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']