# books/api_urls.py
from django.urls import path
from .api_views import BookListCreateAPIView

urlpatterns = [
    path('', BookListCreateAPIView.as_view(), name='book-list-create'),
]