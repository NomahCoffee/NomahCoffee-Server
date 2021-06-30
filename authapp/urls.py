from django.urls import path, include
from authapp import views
from django.conf.urls import url

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('superusers/', views.SuperuserList.as_view(), name='superuser-list'),
    path('staff/', views.StaffList.as_view(), name='staff-list'),
    url(r'^add_to_cart/(?P<upk>[0-9]+)/(?P<cpk>[0-9]+)/(?P<qpk>[0-9]+)/$', views.add_to_cart),
    url(r'^delete_from_cart/(?P<upk>[0-9]+)/(?P<cpk>[0-9]+)/$', views.delete_from_cart)
]