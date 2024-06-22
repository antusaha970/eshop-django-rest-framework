from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, ProductImages
from .serializers import ProductSerializer, ProductImageSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .filters import ProductFilter
from rest_framework import status
# Create your views here.


@api_view(["get"])
def get_products(request):

    # filterset
    filterset = ProductFilter(
        request.GET, queryset=Product.objects.all().order_by("id"))
    count = filterset.qs.count()

    # pagination
    resultPerPage = 10
    paginator = PageNumberPagination()
    paginator.page_size = resultPerPage
    queryset = paginator.paginate_queryset(filterset.qs, request)

    # serializer
    serializer = ProductSerializer(queryset, many=True)

    return Response({
        'count': count,
        'resultPerPage': resultPerPage,
        'products': serializer.data
    })


@api_view(["get"])
def get_product(request, pk):

    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)

    return Response({'product': serializer.data})


@api_view(["post"])
def upload_product_image(request):
    product_id = request.data.get('product')
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    images = request.FILES.getlist('images')
    serializer_data = []  # Create a list to hold dictionaries

    for image in images:
        # Create a dictionary for each image
        data = {'product': product.id, 'image': image}
        serializer_data.append(data)

    serializer = ProductImageSerializer(data=serializer_data, many=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
