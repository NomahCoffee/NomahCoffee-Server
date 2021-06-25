from django.urls import path, include
from authapp import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('superusers/', views.SuperuserList.as_view(), name='superuser-list'),
    path('staff/', views.StaffList.as_view(), name='staff-list')
]