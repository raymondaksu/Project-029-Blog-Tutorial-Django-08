from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ChangePasswordSerializer, RegisterSerializer
from django.contrib.auth import update_session_auth_hash
from .permissions import NotAuthenticated
from .throttles import RegisterThrottle

from .serializers import UserSerializer

class ProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id = self.request.user.id)
        return obj
    
    def perform_update(self, serializer):
        serializer.save(user = self.request.user)

class UpdatePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {
            "old_password": request.data["old_password"],
            "new_password": request.data["new_password"],
        }
    
        serializer = ChangePasswordSerializer(data = data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password" : "wrong_password"}, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            # It provides not logged of after change password
            update_session_auth_hash(request, self.object)
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(serializer.errors, status = status.HTTP_406_NOT_ACCEPTABLE)

#Create User
class CreateUserView(CreateAPIView):
    throttle_classes = [RegisterThrottle]
    model = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (NotAuthenticated,)