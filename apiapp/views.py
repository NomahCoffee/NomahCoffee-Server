from django.shortcuts import render

from .models import Coffee
from .serializers import CoffeeSerializer

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
        'coffees': reverse('coffee-list', request=request, format=format)
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