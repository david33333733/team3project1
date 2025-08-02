from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from reviews.models import Review
from books.models import Book  # ✅ 도서 정보 가져오기
from reviews.forms import ReviewForm  # ✅ 리뷰 폼 임포트

def index(request):
    recent_reviews = Review.objects.select_related('book', 'user').order_by('-created_at')[:4]
    return render(request, 'index.html', {
        'recent_reviews': recent_reviews,
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def review_create(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', pk=book_id)  # ✅ URL 패턴에 맞춰 'pk'로 변경
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form})