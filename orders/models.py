from django.db import models
from product.models import Product
from django.contrib.auth.models import User
# Create your models here.


class Payment_Status(models.TextChoices):
    PAID = "PAID"
    UNPAID = "UNPAID"


class Order_Status(models.TextChoices):
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"


class Payment_Mode(models.TextChoices):
    COD = "COD"
    CARD = "CARD"


class Order(models.Model):
    street = models.CharField(max_length=500, default="", blank=False)
    city = models.CharField(max_length=100, default="", blank=False)
    state = models.CharField(max_length=100, default="", blank=False)
    zip_code = models.CharField(max_length=100, default="", blank=False)
    phone_number = models.CharField(max_length=100, default="", blank=False)
    country = models.CharField(max_length=100, default="", blank=False)
    total_amount = models.DecimalField(max_digits=7, decimal_places=2)
    payment_status = models.CharField(
        max_length=100, choices=Payment_Status.choices, default=Payment_Status.UNPAID)
    status = models.CharField(
        max_length=100, choices=Order_Status.choices, default=Order_Status.PROCESSING)
    payment_mode = models.CharField(
        max_length=100, choices=Payment_Mode.choices, default=Payment_Mode.COD)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orderItems")
    name = models.CharField(max_length=200, default="", blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)

    def __str__(self) -> str:
        return self.name
