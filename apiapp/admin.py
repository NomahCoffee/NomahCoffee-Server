from django.contrib import admin
from .models import Coffee, StoreHours, StoreLocation

# Register your models here.

admin.site.register(Coffee)
admin.site.register(StoreHours)
admin.site.register(StoreLocation)