from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import User, Cart

# Create your serializers here

class CartSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Cart.objects.create(**validated_data)

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