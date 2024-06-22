from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from .filters import ProductFilter
# Create your views here.


@api_view(["get"])
def get_products(request):

    filterset = ProductFilter(
        request.GET, queryset=Product.objects.all().order_by("id"))

    serializer = ProductSerializer(filterset.qs, many=True)

    return Response({'products': serializer.data})


@api_view(["get"])
def get_product(request, pk):

    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)

    return Response({'product': serializer.data})
