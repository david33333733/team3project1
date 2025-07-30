from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    review_id = models.AutoField(
        primary_key=True,
        verbose_name="리뷰 ID"
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="도서"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="작성자"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="평점"
    )
    content = models.CharField(
        max_length=200,
        verbose_name="리뷰 내용"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="작성일"
    )

    class Meta:
        verbose_name = "리뷰"
        verbose_name_plural = "리뷰 목록"
        ordering = ["-created_at"]

    def str(self):
        return f"[{self.book.title}] {self.user.username}님의 리뷰"
