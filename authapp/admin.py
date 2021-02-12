from django.contrib import admin
from .models import User, Cart

# Register your models here.

class CartListInline(admin.StackedInline):
    model = Cart
    extra = 0

class UserAdmin(admin.ModelAdmin):
    inlines = [
        CartListInline,
    ]

admin.site.register(User, UserAdmin)