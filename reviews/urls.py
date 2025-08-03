from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReviewViewSet,
    review_detail,
    review_create,
    review_update,
    review_delete,
)

# DRF용 라우터
router = DefaultRouter()
router.register(r'api', ReviewViewSet, basename='review')

urlpatterns = [
    # ✅ HTML 기반 뷰
    path('create/<int:book_id>/', review_create, name='review_create'),         # 리뷰 작성
    path('<int:pk>/', review_detail, name='review_detail'),                     # 리뷰 상세
    path('<int:pk>/edit/', review_update, name='review_update'),               # 리뷰 수정
    path('<int:pk>/delete/', review_delete, name='review_delete'),             # 리뷰 삭제

    # ✅ DRF API 경로
    path('api/', include(router.urls)),
]
