from django.urls import path
from . import views
urlpatterns = [
    path('products/', views.get_products, name="all_products"),
    path('products/<str:pk>/', views.get_product, name="get_product"),
]
