from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView, CreateAPIView)
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin

from post.api.paginations import PostPagination
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from post.models import Post
from .serializers import PostSerializer, PostUpdateCreateSerializer


class PostListAPIView(ListAPIView, CreateModelMixin):
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ('title', 'content')
    pagination_class = PostPagination

    def get_queryset(self):
        queryset = Post.objects.filter(draft=False)
        return queryset
    
    #---------create model mixin adding----
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    
    # def perform_create(self, serializer):
    #     serializer.save(user = self.request.user)


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    # www.example.com/api/post/detail/2121-sadhksa5d46-sadkl


# class PostDeleteAPIView(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsOwner]


class PostUpdateAPIView(RetrieveUpdateAPIView, DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


class PostCreateAPIView(CreateAPIView, ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    permission_classes = [IsAuthenticated]

    #---------------list model mixin------------------
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(user=self.request.user)
        # this field might be used send email "Welcome etc"
