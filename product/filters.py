from django_filters import rest_framework as filter
from .models import Product


class ProductFilter(filter.FilterSet):
    min_price = filter.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filter.NumberFilter(field_name="price", lookup_expr='lte')
    keyword = filter.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ("brand", "category", "min_price", "max_price", "keyword")
