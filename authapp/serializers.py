from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import *

# Create your serializers here

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        field = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'phone']