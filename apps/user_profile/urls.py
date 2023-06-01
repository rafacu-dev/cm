from django.urls import path
from .views import GetUserProfileView,UpdateUserProfileView,UploadDataUserProfileView,UploadContactUserProfileView

urlpatterns = [
    path('user', GetUserProfileView.as_view()),
    path('update', UpdateUserProfileView.as_view()),
    path('upload-data', UploadDataUserProfileView.as_view()),
    path('upload-contact', UploadContactUserProfileView.as_view()),
]
