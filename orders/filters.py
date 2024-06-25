from django_filters import rest_framework as filter
from .models import Order


class OrderFilter(filter.FilterSet):
    class Meta:
        model = Order
        fields = ("payment_status", "status", "payment_mode", "user")
