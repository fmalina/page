from django.urls import path
from . import views

urlpatterns = [
    path('feed', views.feed, name='feed'),
]
