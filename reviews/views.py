from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

from .models import Review
from .serializers import ReviewSerializer
from books.models import Book


# ✅ 커스텀 권한 클래스
class IsReviewAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_staff


# ✅ HTML 리뷰 상세 페이지
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})


# ✅ HTML 리뷰 작성 폼 처리
@login_required
def review_create(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
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
            return redirect("book_detail", book_id=book.book_id)

    return render(request, "reviews/review_form.html", {
        "book": book,
        "review": None
    })


# ✅ HTML 리뷰 수정 처리
@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)

    # 🔐 작성자 삭제되었을 가능성 처리
    review_user = review.user  # None일 수 있음
    if review_user is not None:
        if request.user != review_user and not request.user.is_staff:
            return HttpResponseForbidden("수정 권한이 없습니다.")
    elif not request.user.is_staff:
        return HttpResponseForbidden("작성자가 삭제된 리뷰는 관리자만 수정할 수 있습니다.")

    if request.method == "POST":
        rating = request.POST.get("rating")
        content = request.POST.get("content")
        if rating and content:
            review.rating = rating
            review.content = content
            review.save()
            return redirect("book_detail", book_id=review.book.book_id)

    return render(request, "reviews/review_form.html", {
        "review": review
    })


# ✅ HTML 리뷰 삭제 처리
@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)

    review_user = review.user
    if review_user is not None:
        if request.user != review_user and not request.user.is_staff:
            return HttpResponseForbidden("삭제 권한이 없습니다.")
    elif not request.user.is_staff:
        return HttpResponseForbidden("작성자가 삭제된 리뷰는 관리자만 삭제할 수 있습니다.")

    if request.method == "POST":
        book_id = review.book.book_id
        review.delete()
        return redirect("book_detail", book_id=book_id)

    return render(request, "reviews/review_confirm_delete.html", {"review": review})


# ✅ DRF API용 ViewSet
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewAuthorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Review.objects.all()
        book_id = self.request.query_params.get('book_id')
        if book_id is not None:
            queryset = queryset.filter(book_id=book_id)
        return queryset
