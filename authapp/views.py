from warnings import catch_warnings
from django.shortcuts import render

from .models import User, Cart
from apiapp.models import Coffee
from .serializers import CartSerializer, UserCreateSerializer

from rest_framework import mixins, generics, permissions, renderers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated

from django.core import serializers

from django.http.response import JsonResponse

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

@api_view(['POST', 'PUT', 'DELETE'])
def update_cart(request):
    if request.method == 'POST':
        # Make sure to have the user ID before setting a user object
        userId = request.POST.get('userId')
        if not userId:
            return JsonResponse({'message': 'The user id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=userId)
        except User.DoesNotExist: 
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Make sure to have the coffee ID before setting a coffee object
        coffeeId = request.POST.get('coffeeId')
        if not userId:
            return JsonResponse({'message': 'The coffee id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            coffee = Coffee.objects.get(pk=coffeeId)
        except Coffee.DoesNotExist:
            return JsonResponse({'message': 'The coffee does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Get quantity
        quantity = request.POST.get('quantity')
        if not quantity:
            return JsonResponse({'message': 'The quantity does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_serializer = CartSerializer()
        newCartItem = {
            "coffee": coffee,
            "person": user,
            "quantity": quantity
        }
        cart_serializer.create(newCartItem)

        # Return the user object associated with the newly added cart item
        user_serializer = UserCreateSerializer(user) 
        return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 

    if request.method == 'PUT':
        # Get quantity
        quantity = request.POST.get('quantity')
        if not quantity:
            return JsonResponse({'message': 'The quantity does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Make sure to have the cart ID before setting the cart object
        cartId = request.POST.get('cartId')
        if not cartId:
            return JsonResponse({'message': 'The cart id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cartItem = Cart.objects.get(pk=cartId)
        except Coffee.DoesNotExist:
            return JsonResponse({'message': 'The cart does not exist'}, status=status.HTTP_404_NOT_FOUND)

        cartItem.quantity = quantity
        cartItem.save()

        # Return the user object associated with the newly updated cart item
        user_serializer = UserCreateSerializer(cartItem.person) 
        return JsonResponse(user_serializer.data, status=status.HTTP_200_OK) 


    if request.method == 'DELETE':
        # Make sure to have the cart ID before setting the cart object
        cartId = request.POST.get('cartId')
        if not cartId:
            return JsonResponse({'message': 'The cart id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cartItem = Cart.objects.get(pk=cartId)
        except Coffee.DoesNotExist:
            return JsonResponse({'message': 'The cart does not exist'}, status=status.HTTP_404_NOT_FOUND)

        cartItem.delete()
        
        # Return the user object associated with the newly updated cart item
        user_serializer = UserCreateSerializer(cartItem.person) 
        return JsonResponse(user_serializer.data, status=status.HTTP_200_OK) 
