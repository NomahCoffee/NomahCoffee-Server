from django.urls import path, include
from django.conf.urls import url
from authapp import views

# Used a mixture of url patters. path() comes from the DjangoRestFramework
# and url() is out of the box Django code.
urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('superusers/', views.SuperuserList.as_view(), name='superuser-list'),
    path('staff/', views.StaffList.as_view(), name='staff-list'),
    url(r'update_cart/', views.update_cart),
    url(r'payment_sheet/', views.payment_sheet)
]