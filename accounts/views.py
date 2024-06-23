from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
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
