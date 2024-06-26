from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
import stripe.error
import stripe.webhook
from .models import Order, OrderItem
from product.models import Product
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404
from .filters import OrderFilter
from rest_framework.pagination import PageNumberPagination
import stripe
from django.contrib.auth.models import User

import environ
env = environ.Env()
environ.Env.read_env()
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


def get_current_host(request):
    protocol = request.is_secure() and "https" or "http"
    host = request.get_host()
    return f"{protocol}://{host}/"


stripe.api_key = env("STRIPE_SECRET_KEY")


@api_view(["post"])
@permission_classes([IsAuthenticated])
def checkout_order(request):
    YOUR_DOMAIN = get_current_host(request)

    data = request.data
    user = request.user

    orderItems = data['orderItems']

    shipping_details = {
        'street': data['street'],
        'city': data['city'],
        'state': data['state'],
        'zip_code': data['zip_code'],
        'phone_number': data['phone_number'],
        'country': data['country'],
        'user': user.id
    }

    checkout_order_items = []
    for item in orderItems:
        checkout_order_items.append(
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['name'],
                        'metadata': {'product_id': item['product']}
                    },
                    'unit_amount': item['price']*100
                },
                'quantity': item['quantity'],
            }
        )
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        metadata=shipping_details,
        line_items=checkout_order_items,
        customer_email=user.email,
        mode='payment',
        success_url=YOUR_DOMAIN,
        cancel_url=YOUR_DOMAIN,
    )

    return Response({'session': session})


@api_view(["post"])
def stripe_webhook(request):
    STRIPE_WEBHOOK_KEY = env("STRIPE_WEBHOOK_KEY")
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_KEY
        )
    except ValueError as e:
        return Response({'errors': "Invalid Payload"}, status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        return Response({'errors': "Invalid Signature"}, status=status.HTTP_400_BAD_REQUEST)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        line_items = stripe.checkout.Session.list_line_items(session['id'])
        print("line items", line_items)
        price = session['amount_total'] / 100

        order = Order.objects.create(
            user=User(session.metadata.user),
            city=session.metadata.city,
            country=session.metadata.country,
            phone_number=session.metadata.phone_number,
            state=session.metadata.state,
            street=session.metadata.street,
            zip_code=session.metadata.zip_code,
            total_amount=price,
            payment_mode="CARD",
            payment_status="COD"
        )

        for item in line_items['data']:
            print("item", item)
            line_product = stripe.Product.retrieve(item.price.product)
            product_id = line_product.metadata.product_id
            product = Product.objects.get(id=product_id)

            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                price=item.price.unit_amount/100,
                quantity=item.quantity
            )
            product.stock -= item.quantity
            product.save()

        return Response({'details': "Payment successfull"}, status=status.HTTP_200_OK)
