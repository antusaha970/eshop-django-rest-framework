from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from product.models import Product
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404
from .filters import OrderFilter
from rest_framework.pagination import PageNumberPagination
# Create your views here.


@api_view(['post'])
@permission_classes([IsAuthenticated])
def make_order(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'errors': "You do not have any order items"}, status=status.HTTP_400_BAD_REQUEST)

    else:
        total_amount = sum(item['price']*item['quantity']
                           for item in orderItems)

        order = Order.objects.create(
            street=data['street'],
            city=data['city'],
            state=data['state'],
            zip_code=data['zip_code'],
            phone_number=data['phone_number'],
            country=data['country'],
            total_amount=total_amount,
            user=user
        )

        order.save()

        for item in orderItems:
            product = Product.objects.get(id=item['product'])

            oderItem = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity=item['quantity'],
                price=item['price']
            )
            product.stock -= item['quantity']
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_all_orders(request):

    filterset = OrderFilter(
        request.GET, queryset=Order.objects.all().order_by('id'))
    count = filterset.qs.count()
    # pagination
    resultPerPage = 1
    paginator = PageNumberPagination()
    paginator.page_size = resultPerPage
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = OrderSerializer(queryset, many=True)
    return Response({'count': count, 'resultPerPage': resultPerPage, 'orders': serializer.data})


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_single_order(request, pk=None):
    order = get_object_or_404(Order, id=pk)

    serializer = OrderSerializer(order, many=False)
    return Response({'order': serializer.data})


@api_view(['put'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_order(request, pk=None):
    order = get_object_or_404(Order, id=pk)
    data = request.data['status']
    order.status = data
    order.save()
    serializer = OrderSerializer(order, many=False)
    return Response({'order': serializer.data})


@api_view(['delete'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_order(request, pk=None):
    order = get_object_or_404(Order, id=pk)
    order.delete()
    return Response({'details': "order deleted"}, status=status.HTTP_204_NO_CONTENT)
