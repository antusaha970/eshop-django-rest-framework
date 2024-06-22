from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.TextChoices):
    ELECTRONICS = "Electronics"
    LAPTOPS = "Laptops"
    HOME = "Home"
    ART = "Art"
    FOOD = "Food"
    KITCHEN = "Kitchen"
    TV = "TV"
    BOOKS = "Books"


class Product(models.Model):
    name = models.CharField(max_length=300, default="")
    description = models.TextField(default="")
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    brand = models.CharField(max_length=200, default="")
    category = models.CharField(max_length=200, choices=Category.choices)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", null=True)
    image = models.ImageField(upload_to="product_image/")
