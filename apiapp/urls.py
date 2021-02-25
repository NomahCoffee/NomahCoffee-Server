from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.api_root),
    path('coffee/', views.CoffeeList.as_view(), name='coffee-list'),
    path('coffee/<int:pk>/', views.CoffeeDetail.as_view(), name='coffee-detail'),
    path('hours/', views.StoreHoursList.as_view(), name='hours-list'),
    path('locations/', views.StoreLocationsList.as_view(), name='locations-list'),
]