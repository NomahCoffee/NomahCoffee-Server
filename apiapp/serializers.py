from rest_framework import serializers
from .models import Coffee

# Create your serializers here

class CoffeeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Coffee
        fields = ['url', 'id', 'owner', 'name', 'price', 'image', 'description', 'in_stock']