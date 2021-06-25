from django.shortcuts import render

from .models import Coffee, StoreHours, StoreLocation
from .serializers import CoffeeSerializer, StoreHoursSerializer, StoreLocationSerializer

from rest_framework import mixins, generics, permissions, renderers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'superusers': reverse('superuser-list', request=request, format=format),
        'staff': reverse('staff-list', request=request, format=format),
        'coffees': reverse('coffee-list', request=request, format=format),
        'hours': reverse('hours-list', request=request, format=format),
        'locations': reverse('locations-list', request=request, format=format)
    })

class CoffeeList(generics.ListCreateAPIView):
    queryset = Coffee.objects.all()
    serializer_class = CoffeeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CoffeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coffee.objects.all()
    serializer_class = CoffeeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class StoreHoursList(generics.ListCreateAPIView):
    queryset = StoreHours.objects.all()
    serializer_class = StoreHoursSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StoreLocationsList(generics.ListCreateAPIView):
    queryset = StoreLocation.objects.all()
    serializer_class = StoreLocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
