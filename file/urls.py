
from django.urls import path

from .views import MainPictureUploadView

urlpatterns = [
    path('main-picture', MainPictureUploadView.as_view(), name='main-picture'),
]
