from django.urls import path
from .views import GetMarketView

urlpatterns = [
    path('get', GetMarketView.as_view()),
]
