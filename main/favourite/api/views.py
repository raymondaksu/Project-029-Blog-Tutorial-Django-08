from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from favourite.models import Favourite
from .serializers import FavouriteListCreateAPISerializer, FavouriteAPISerializer
from .paginations import FavouritePagination
from .permissions import IsOwner

class FavouriteListCreateAPIView(ListCreateAPIView):
    serializer_class = FavouriteListCreateAPISerializer
    pagination_class = FavouritePagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class FavouriteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteAPISerializer
    permission_classes = [IsOwner]
    lookup_field = 'pk'





