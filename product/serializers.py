from rest_framework import serializers
from .models import Product, ProductImages, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        extra_kwargs = {
            "comment": {"required": True, },
            "rating": {"required": True, },
        }


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField('get_reviews', read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            "name": {"required": True, },
            "description": {"required": True, },
            "price": {"required": True, },
            "brand": {"required": True, },
            "category": {"required": True, },
            "rating": {"required": True, },
            "stock": {"required": True, },
        }

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
