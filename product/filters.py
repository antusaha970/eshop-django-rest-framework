from django_filters import rest_framework as filter
from .models import Product


class ProductFilter(filter.FilterSet):
    min_price = filter.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filter.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ("brand", "category")
