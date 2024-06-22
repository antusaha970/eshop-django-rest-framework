from django.urls import path
from . import views
urlpatterns = [
    path('products/', views.get_products, name="all_products"),
    path('products/new/', views.make_product, name="make_product"),
    path('product/upload_images/', views.upload_product_image,
         name="upload_product_image"),
    path('products/<str:pk>/', views.get_product, name="get_product"),
    path('products/<str:pk>/update', views.update_product, name="update_product"),
]
