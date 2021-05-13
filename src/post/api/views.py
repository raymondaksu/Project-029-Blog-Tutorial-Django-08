from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView, CreateAPIView)

from post.api.paginations import PostPagination
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from post.models import Post
from .serializers import PostSerializer, PostUpdateCreateSerializer


class PostListAPIView(ListAPIView):
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ('title', 'content')
    pagination_class = PostPagination

    def get_queryset(self):
        queryset = Post.objects.filter(draft=False)
        return queryset


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    # www.example.com/api/post/detail/2121-sadhksa5d46-sadkl


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # this field might be used send email "Welcome etc"
