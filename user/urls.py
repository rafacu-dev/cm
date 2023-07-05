from django.urls import path
from .views import UserVerify

urlpatterns = [
    path('verify/', UserVerify.as_view()),
]
