from django.db import models
from django.contrib.auth.models import AbstractUser
from apiapp.models import Coffee

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    phone = models.CharField(null=True, max_length=255)
    REQUIRED_FIELDS = ['username', 'phone', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    def get_username(self):
        return self.email

class Cart(models.Model):
    coffee = models.ForeignKey('apiapp.Coffee', on_delete=models.CASCADE)
    person = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.coffee.name + " | Count: {}".format(self.quantity)
    
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart'