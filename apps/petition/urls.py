from django.urls import path
from .views import PetitionView, StaticView

urlpatterns = [
    path('new', PetitionView.as_view()),
    path('update', PetitionView.as_view()),
    path('delete', PetitionView.as_view()),
    path('static', StaticView.as_view()),
]
