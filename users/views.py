from core.utils.BASEModelViewSet import BaseModelViewSet
from core.permissions import IsUserSelfOrAdmin
from .models import ProfileImage, User
from .serializers import ProfileImageSerializer, UserSerializer

# class ProfileImageViewSet(ModelViewSet):
#     serializer_class = ProfileImageSerializer
#     permission_classes = [IsUserSelfOrAdmin]

#     def get_queryset(self):
#         return ProfileImage.objects.filter(user_id=self.kwargs.get('user_pk'))

#     def perform_create(self, serializer):
#         serializer.save(user_id=self.kwargs.get('user_pk'))

class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserSelfOrAdmin]