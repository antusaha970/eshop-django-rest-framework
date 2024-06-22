from rest_framework import serializers
from .models import Product, ProductImages


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

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
