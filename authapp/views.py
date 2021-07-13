from warnings import catch_warnings
from django.shortcuts import render
from django.conf import settings

from .models import User, Cart
from apiapp.models import Coffee
from .serializers import CartSerializer, UserCreateSerializer, CurrentUserSerializer

from rest_framework import mixins, generics, permissions, renderers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated

from django.http.response import JsonResponse

import stripe

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
    # In the case of a POST, the client must provide a the following. This handles the
    # case where a completely new cart item will be added to a user's cart.
    #
    # - userId: the ID of the user to which they intent to update the cart of
    # - coffeeId: the ID of the coffee item that they intent to add to cart
    # - quantity: an integer representing the number of this specific coffee to be added to cart
    if request.method == 'POST':

        # Make sure the request contains a userId
        userId = request.POST.get('userId')
        if not userId:
            return JsonResponse({'message': 'The user id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Grab the specific user by the userId passed by the request
        try:
            user = User.objects.get(pk=userId)
        except User.DoesNotExist: 
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Make sure the request contains a coffeeId
        coffeeId = request.POST.get('coffeeId')
        if not userId:
            return JsonResponse({'message': 'The coffee id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Grab the specific coffee by the coffeeId passed by the request
        try:
            coffee = Coffee.objects.get(pk=coffeeId)
        except Coffee.DoesNotExist:
            return JsonResponse({'message': 'The coffee does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Get quantity
        quantity = request.POST.get('quantity')
        if not quantity:
            return JsonResponse({'message': 'The quantity does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new a new cart item
        newCartItem = {
            "coffee": coffee,
            "person": user,
            "quantity": quantity
        }
        cart_serializer = CartSerializer()
        cart_serializer.create(newCartItem)

        # Return the user object associated with the newly added cart item
        user_serializer = CurrentUserSerializer(user)
        return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 

    # In the case of a PUT, the client must provide a the following. This handles the
    # case where a the quantity value of an existing cart item will be edited.
    #
    # - cartId: the ID of the cart to which they intent to edit the quantity of
    # - quantity: an integer representing the number of this specific coffee to be added to cart
    if request.method == 'PUT':

        # Make sure the request contains a cartId
        cartId = request.POST.get('cartId')
        if not cartId:
            return JsonResponse({'message': 'The cart id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Grab the specific cart item by the cartId passed by the request
        try:
            cartItem = Cart.objects.get(pk=cartId)
        except Coffee.DoesNotExist:
            return JsonResponse({'message': 'The cart does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get quantity
        quantity = request.POST.get('quantity')
        if not quantity:
            return JsonResponse({'message': 'The quantity does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the quantity of the specific cart item
        cartItem.quantity = quantity
        cartItem.save()

        # Return the user object associated with the newly added cart item
        user_serializer = CurrentUserSerializer(cartItem.person)
        return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 

    # In the case of a DELETE, the client must provide a the following. This handles the
    # case where one spefic cart item is to be deleted from a users cart.
    #
    # - cartId: the ID of the cart to which they intent to delete
    if request.method == 'DELETE':

        # Make sure the request contains a cartId
        cartId = request.POST.get('cartId')
        if not cartId:
            return JsonResponse({'message': 'The cart id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Grab the specific cart item by the cartId passed by the request
        try:
            cartItem = Cart.objects.get(pk=cartId)
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'The cart does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the cart item from cart
        cartItem.delete()

        # Return the user object associated with the newly added cart item
        user_serializer = CurrentUserSerializer(cartItem.person)
        return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 

@api_view(['DELETE'])
def clear_cart(request):
    # In the case of a DELETE, the client must provide the following. This handles the
    # case where one specific user will have their entire cart cleared.
    #
    # - userId: the ID of the user to which they intent to clear the cart
    if request.method == 'DELETE':

        # Make sure the request contains a userId
        userId = request.POST.get('userId')
        if not userId:
            return JsonResponse({'message': 'The user id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Grab the specific user by the userId passed by the request
        try:
            user = User.objects.get(pk=userId)
        except User.DoesNotExist:
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the user and grab their cart field
        user_serializer = CurrentUserSerializer(user)
        user_cart = user_serializer.data['cart']

        # Loop through each item in cart and delete it
        for cartItem in user_cart:
            try:
                cartItem = Cart.objects.get(pk=cartItem['id'])
                cartItem.delete()
            except Cart.DoesNotExist:
                return JsonResponse({'message': 'A cart item does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
        # Reassign the user serializer to account for the change in the cart done above
        user_serializer = CurrentUserSerializer(user)

        # Return the user object associated with the newly cleared cart
        return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 

@api_view(['POST'])
def payment_sheet(request):
    stripe.api_key = settings.STRIPE_TEST_KEY

    # Make sure the request contains a userId
    userId = request.POST.get('userId')
    if not userId:
        return JsonResponse({'message': 'The user id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    # Grab the specific user by the userId passed by the request
    try:
        user = User.objects.get(pk=userId)

        # Check if the user has a stripe id, if not, they are a new customer
        if user.stripe_id == '':
            # This is a new customer, so create a stripe user and assign their stripe id to their user
            customer = stripe.Customer.create(
                email=user.email,
                name=user.first_name + " " + user.last_name
            )
            # Save the stripe id to the user object
            user.stripe_id = customer['id']
            user.save()
        else:
            # This is a returning customer
            customer = stripe.Customer.retrieve(user.stripe_id)

    except User.DoesNotExist: 
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Set up the user's ephemeral key
    ephemeralKey = stripe.EphemeralKey.create(
        customer=customer['id'],
        stripe_version='2020-08-27',
    )

    # Serialize the user and grab their cart field, which should be an updated cart for this specific user 
    user_serializer = CurrentUserSerializer(user)
    user_cart = user_serializer.data['cart']

    # Tally up the total price of the cart and update the metadata for the payment intent
    totalPrice = 0
    paymentMetadata = {}
    for cartItem in user_cart:
        try:
            cartItem = Cart.objects.get(pk=cartItem['id'])
            totalPrice += cartItem.coffee.price * cartItem.quantity
            paymentMetadata[cartItem.coffee.name + " (" + str(cartItem.quantity) + ")"] = "${:,.2f}".format(float(cartItem.coffee.price * cartItem.quantity))
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'A cart item does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    # Create a payment intent with a total amount, currency, and customer id
    paymentIntent = stripe.PaymentIntent.create(
        amount=int(totalPrice * 100),
        currency='usd',
        customer=customer['id'],
        receipt_email=user.email,
        metadata=paymentMetadata
    )

    # Create a dictionary to send back to the client with pertinent info to trigger a payment sheet
    dict = {
        "paymentIntent": paymentIntent.client_secret,
        "ephemeralKey": ephemeralKey.secret,
        "customer": customer.id
    }
    return JsonResponse(dict)