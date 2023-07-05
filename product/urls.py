from django.urls import path
from .views import ProductView,ProductsView

urlpatterns = [
    path('new', ProductView.as_view()),
    path('update', ProductView.as_view()),
    path('delete', ProductView.as_view()),
    path('get', ProductView.as_view()),
    path('get-all', ProductsView.as_view()),
]
