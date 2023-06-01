from django.urls import path

from .views import CommentsProductView

urlpatterns = [
    path('get', CommentsProductView.as_view()),
    path('new', CommentsProductView.as_view()),
    path('update', CommentsProductView.as_view())
]
