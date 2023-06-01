from django.urls import path
from .views import GetAddressGeopy,GetDirections

urlpatterns = [
    path('address',GetAddressGeopy.as_view(),name = "GetAddress"),
    path('rute',GetDirections.as_view(),name = "GetDirections"),
]