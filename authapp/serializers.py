from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import User, Cart

# Create your serializers here

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'quantity', 'coffee']
        depth = 1

class UserCreateSerializer(UserCreateSerializer):
    cart = CartSerializer(many=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'phone', 'cart']
        depth = 2