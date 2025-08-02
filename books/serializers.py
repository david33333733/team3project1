from rest_framework import serializers
from .models import Book
from authors.models import Author
from reviews.serializers import ReviewSerializer

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author_id.author_name', read_only=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), 
        write_only=True, 
        source='author_id'
    )
    average_rating = serializers.FloatField(read_only=True)
    rating_std_dev = serializers.FloatField(read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('book_id', 'title', 'description', 'publication_date', 'created_at', 'author', 'author_name', 'average_rating', 'rating_std_dev', 'reviews')

    def get_reviews(self, obj):
        reviews = obj.reviews.order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
        