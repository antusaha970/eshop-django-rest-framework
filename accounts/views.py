from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from django.core.mail import send_mail
# Create your views here.


@api_view(["post"])
def sing_up_user(request):
    data = request.data
    serializer = SignUpSerializer(data=data)
    if serializer.is_valid():
        if not User.objects.filter(username=data["email"]).exists():
            user = User.objects.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                username=data["email"],
                password=make_password(data["password"]),
            )
            return Response({"details": "User created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['post'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['put'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.email = data["email"]
    user.username = data["username"]

    if data['password'] != "":
        user.password = make_password(data["password"])

    user.save()
    serializer = UserSerializer(user)
    return Response(serializer.data)


def get_current_host(request):
    protocol = request.is_secure() and "https" or "http"
    host = request.get_host()
    return f"{protocol}://{host}/"


@api_view(["post"])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])
    token = get_random_string(40)
    expire_date = datetime.now()+timedelta(minutes=30)

    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date

    user.profile.save()

    host = get_current_host(request)
    link = f"{host}api/reset_password/{token}/"
    body = f"Your password reset link is: {link}"

    send_mail("Password reset link", body, "noreply@ehop.com", [data['email']])

    return Response({"details": "Password reset link send to your email address"})


@api_view(['post'])
def reset_password(request, token):
    data = request.data
    user = get_object_or_404(User, profile__reset_password_token=token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    if data['password'] != data["confirm_password"]:
        return Response({"error": "Password did not match"}, status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(data["password"])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.save()
    user.profile.save()

    return Response({"details": "Password updated successfully"}, status=status.HTTP_200_OK)
