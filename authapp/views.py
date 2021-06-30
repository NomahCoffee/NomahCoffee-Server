from django.shortcuts import render

from .models import User, Cart
from apiapp.models import Coffee
from .serializers import CartSerializer, UserCreateSerializer

from rest_framework import mixins, generics, permissions, renderers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated

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
 
@api_view(['POST'])
def add_to_cart(request, upk, cpk, qpk):
    # Get the User object by id
    try: 
        user = User.objects.get(pk=upk)
    except User.DoesNotExist: 
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Get the coffee object by id
    try:
        coffee = Coffee.objects.get(pk=cpk)
    except Coffee.DoesNotExist:
        return JsonResponse({'message': 'The coffee does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get the quantity
    quantity = qpk

    if request.method == 'POST':
        # print(user, coffee, quantity)
        cart_serializer = CartSerializer()
        newCartItem = {
            "coffee": coffee,
            "person": user,
            "quantity": quantity
        }
        cart_serializer.create(newCartItem)
 
        return JsonResponse(status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_from_cart(request, upk, cpk):
    # Get the User object by id
    try: 
        user = User.objects.get(pk=upk)
    except User.DoesNotExist: 
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Get the cart object by id
    try:
        cartItem = Cart.objects.get(pk=cpk)
    except Coffee.DoesNotExist:
        return JsonResponse({'message': 'The cart does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        count = cartItem.delete()
        return JsonResponse({'message': '{} cart items were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)