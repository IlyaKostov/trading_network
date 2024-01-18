from rest_framework import serializers

from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор создания новых пользователей"""
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Создание нового пользователя"""
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
