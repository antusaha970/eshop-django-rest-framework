from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField('get_order_items')

    class Meta:
        model = Order
        fields = "__all__"

    def get_order_items(self, obj):
        orderItems = obj.orderItems.all()
        serializer = OrderItemSerializer(orderItems, many=True)
        return serializer.data
