from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.serializers import CreateUserSerializer


class RegisterAPIView(CreateAPIView):
    """Регистрация пользователей"""

    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]
