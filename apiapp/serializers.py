from rest_framework import serializers
from .models import Coffee, StoreHours, StoreLocation

# Create your serializers here

class CoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coffee
        fields = ['url', 'id', 'name', 'price', 'image', 'description', 'in_stock']

class StoreHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreHours
        fields = ['day', 'from_hour', 'to_hour', 'closed']

class StoreLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreLocation
        fields = ['name', 'image', 'street', 'city', 'state', 'zip_code']