# books/api_views.py
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by('title')  # 제목 오름차순 정렬
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']           # 검색 대상 필드
    ordering_fields = ['title']         # 정렬 가능 필드
