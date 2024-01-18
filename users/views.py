from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny


class RegisterAPIView(CreateAPIView):
    """Регистрация пользователей"""

    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]
