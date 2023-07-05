from django.urls import path
from .views import PosterView,StaticView

urlpatterns = [
    path('new', PosterView.as_view()),
    path('update', PosterView.as_view()),
    path('delete', PosterView.as_view()),
    path('static', StaticView.as_view()),
]
