from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import permissions, viewsets
from django.contrib.auth.decorators import login_required

from .models import Review
from .serializers import ReviewSerializer
from books.models import Book  # Book 모델 import


# ✅ 권한 클래스: 작성자 또는 관리자만 수정/삭제 가능
class IsReviewAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if view.action in ['update', 'partial_update']:
            return obj.user == request.user
        if view.action == 'destroy':
            return obj.user == request.user or request.user.is_staff
        return False


# ✅ HTML 리뷰 상세 페이지
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})


# ✅ HTML 리뷰 작성 폼 처리
@login_required
def review_create(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        rating = request.POST.get("rating")
        content = request.POST.get("content")

        if rating and content:
            Review.objects.create(
                book=book,
                user=request.user,
                rating=rating,
                content=content
            )
            return redirect("book_detail", book_id=book_id)

    return render(request, "reviews/review_form.html", {"book": book})


# ✅ DRF API용 ViewSet
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Review.objects.all()
        book_id = self.request.query_params.get('book_id')
        if book_id is not None:
            queryset = queryset.filter(book_id=book_id)
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsReviewAuthorOrAdmin()]
        return [permissions.AllowAny()]
