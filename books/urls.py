from django.urls import path, include
from .views import book_list, book_detail, special_books, BookViewSet
from rest_framework.routers import DefaultRouter
from book_api.views import review_create  # ✅ 리뷰 작성 뷰

router = DefaultRouter()
router.register(r'api', BookViewSet, basename='book')

urlpatterns = [
    path('', book_list, name='book_list'),
    path('<int:book_id>/', book_detail, name='book_detail'),  # ✅ book_id로 수정
    path('<int:book_id>/review/create/', review_create, name='review_create'),
    path('special/', special_books, name='special_books'),
    path('api/', include(router.urls)),
]
