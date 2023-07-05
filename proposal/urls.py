from django.urls import path
from .views import ProposeProductView

urlpatterns = [
    path('set', ProposeProductView.as_view()),
    path('get', ProposeProductView.as_view()),
    path('delete', ProposeProductView.as_view()),
]
