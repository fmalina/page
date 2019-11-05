from django.urls import path
from listing.page import views as page_views

urlpatterns = [
    path('feed', page_views.feed, name='feed'),
    path('p<int:pk>', page_views.short),
]
