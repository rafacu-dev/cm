from django.urls import path
from .views import NewShopView,UpdateShopView,GetDataShopView

urlpatterns = [
    path('new', NewShopView.as_view()),
    path('update', UpdateShopView.as_view()),
    path('get', GetDataShopView.as_view()),
]
