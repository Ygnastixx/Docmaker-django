from django.urls import path
from .views import fake_user

urlpatterns = [
    path("user/", fake_user),
]