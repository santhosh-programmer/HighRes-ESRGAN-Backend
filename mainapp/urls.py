from django.urls import path
from .views import PhotoAPIView

urlpatterns = [
    path("photo/", PhotoAPIView.as_view())
]