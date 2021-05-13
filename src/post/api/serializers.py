from traceback import print_exception
from rest_framework import serializers
from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="post:detail",
        lookup_field='slug'
    )

    username = serializers.SerializerMethodField(method_name='username_new')
    # username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        ordering = ['-id']
        fields = ['username', 'title', 'content',
                  'image', 'url', 'created', 'modified_by']

    def username_new(self, obj):
        return str(obj.user.username)

    # def get_username(self, obj):
    #     return str(obj.user.username)


class PostUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

    # -----Adding user into a post via following override method------
    # def create(self, validated_data):
    #     return Post.objects.create(user = self.context["request"].user, **validated_data)

    # -----Update post via following override method------
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.content = 'edited'
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.save()
    #     return instance

    # -----Checking single attribute of content-------------
    # def validate_title(self, value):
    #     if value == "oguzhan":
    #         raise serializers.ValidationError("Bu deger olmaz")
    #     return value

    # ------Checking validate all-------------------------
    # def validate(self, attrs):
    #     if attrs["title"] == "oguzhan":
    #         raise serializers.ValidationError("Bu deger valide degil")
    #     return attrs
