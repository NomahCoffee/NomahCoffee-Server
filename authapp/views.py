from django.shortcuts import render

from .models import User
from .serializers import UserCreateSerializer

from rest_framework import mixins, generics, permissions, renderers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class SuperuserList(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_superuser=True)
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StaffList(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
 