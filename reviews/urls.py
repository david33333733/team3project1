from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, review_detail, review_create

router = DefaultRouter()
router.register(r'api', ReviewViewSet, basename='review')

urlpatterns = [
    # ✅ HTML 기반 뷰
    path('create/<int:book_id>/', review_create, name='review_create'),
    path('<int:pk>/', review_detail, name='review_detail'),

    # ✅ DRF API 경로
    path('api/', include(router.urls)),
]
