from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsUserSelfOrAdmin
from .models import ProfileImage
from .serializers import ProfileImageSerializer

# class ProfileImageViewSet(ModelViewSet):
#     serializer_class = ProfileImageSerializer
#     permission_classes = [IsUserSelfOrAdmin]

#     def get_queryset(self):
#         return ProfileImage.objects.filter(user_id=self.kwargs.get('user_pk'))

#     def perform_create(self, serializer):
#         serializer.save(user_id=self.kwargs.get('user_pk'))