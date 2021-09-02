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
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'cart']
        depth = 2

class CurrentUserSerializer(UserSerializer):
    cart = CartSerializer(many=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'stripe_id', 'cart']
        depth = 2