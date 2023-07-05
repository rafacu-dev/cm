from django.urls import path
from .views import ShoppingView,BuyView,SaleView,CompleteShoppingView

urlpatterns = [
    path('add', ShoppingView.as_view()),
    path('buy', BuyView.as_view()),
    path('sale', SaleView.as_view()),
    path('completed', CompleteShoppingView.as_view())
]
