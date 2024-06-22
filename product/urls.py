from django.urls import path
from . import views
urlpatterns = [
    path('products/', views.get_products, name="all_products"),
    path('product/upload_images/', views.upload_product_image,
         name="upload_product_image"),
    path('products/<str:pk>/', views.get_product, name="get_product"),
]
